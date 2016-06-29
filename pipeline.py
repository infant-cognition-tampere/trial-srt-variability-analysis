# -*- coding: utf-8 -*-
from tasks import common_to_reactions
from tasks import anonymize_reactions
from tasks import reactions_to_tbt_csv
from tasks import reactions_to_categorical_predictions
from tasks import reactions_to_goldfish_predictions
from tasks import predictions_to_visualization
from tasks import goldfish_predictions_to_visualization
from tasks import filter_in_complete_sequences
from tasks import filter_in_good_sequences
from tasks import reactions_to_distribution_visualization
from tasks import reactions_to_markov_predictions
from tasks import markov_predictions_to_visualization
from tasks import reactions_to_statistics
from tasks import statistics_to_visualization
from tasks import reactions_to_sequence_visualization
from tasks import combine_predictions_to_csv

from os.path import isfile, getmtime
from glob import glob

#######
# Utils
#######

class PipelineError(Exception):
    pass

def arefiles(paths):
    return all([isfile(f) for f in paths])

def areolder(paths, ref):
    '''True if all the files are older than the reference file'''
    ageref = getmtime(ref)
    ages = [getmtime(p) for p in paths]
    # The smaller the timestamp, the older the file.
    return all([ageref > age for age in ages])

def areyounger(paths, ref):
    '''True if all the files are younger than the reference file'''
    ageref = getmtime(ref)
    ages = [getmtime(p) for p in paths]
    # The smaller the timestamp, the older the file.
    return all([ageref < age for age in ages])

def run(module, input_files, output_files):
    '''
    Run fn.run if
    - some output_files are missing
    - some output_files are older than the module
    - some output_files are older than the input_files
    Do not run if
    - some input_files are missing
    '''
    print('Running ' + module.__name__)
    if arefiles(input_files):
        if arefiles(output_files):
            # If any output is older than module, then module needs to be run.
            # In other words, if all output files are younger, then use cache.
            if areyounger(output_files, module.__file__):
                if all([areolder(input_files, f) for f in output_files]):
                    print('- Result already in cache. Skipping...')
                    return  # skip computation
        return module.run(input_files, output_files)
    else:
        msg = 'Some input files are missing: ' + ', '.join(input_files)
        print(msg)
        print('Aborting...')
        raise PipelineError(msg)

#######
# Main
#######

def pipeline():

    # O = out, I = in

    #  O  gazedata in a project specific format
    #  |
    #  I
    # NOTE:
    # Data needs to be converted to Gazelib's CommonV1 format before analysis.
    # The following task needs to be implemented for that to happen.
    # run(gazedata_to_common, [], [])
    #  O
    #  |
    #  I
    # NOTE:
    # Source data was removed from public release due to privacy concerns.
    # To run the analysis from the source data, provide the source data files
    # in CommonV1 format and uncomment.
    # run(common_to_reactions,
    #    glob('data/cg8mo-common/*.common.json'),
    #    ['data/reactions-unanonymized.json'])
    #  O
    #  |
    #  I
    run(anonymize_reactions,
        ['data/reactions-unanonymized.json'],
        ['data/reactions.json'])
    #  O
    #  |__
    #  |  |
    #  |  I
    run(reactions_to_distribution_visualization,
        ['data/reactions.json'],
        ['data/reactions.html'])
    #  |__
    #  |  |
    #  |  I
    run(reactions_to_statistics,
        ['data/reactions.json'],
        ['data/reactions-statistics.json'])
    #  |  O
    #  |  |
    #  |  I
    run(statistics_to_visualization,
        ['data/reactions-statistics.json'],
        ['data/reactions-statistics.html'])
    #  |__
    #  |  |
    #  |  I
    run(reactions_to_tbt_csv,
        ['data/reactions.json'],
        ['data/reactions.csv'])
    #  |
    #  I
    run(filter_in_good_sequences,
        ['data/reactions.json'],
        ['data/reactions-only-good.json'])
    #  O
    #  |________
    #  |        |
    #  |        I
    run(reactions_to_categorical_predictions,
        ['data/reactions-only-good.json'],
        ['data/categorical-predictions.json'])
    #  |        O
    #  |__      |
    #  |  |     |
    #  |  I     |
    run(reactions_to_statistics,
        ['data/reactions-only-good.json'],
        ['data/reactions-only-good-statistics.json'])
    #  |__      |
    #  |  |     |
    #  |  I     |
    run(reactions_to_goldfish_predictions,
        ['data/reactions-only-good.json'],
        ['data/goldfish-predictions.json'])
    #  |  O     |
    #  |  |__   |
    #  |  |  |  |
    #  |  I  |  |
    run(goldfish_predictions_to_visualization,
        ['data/goldfish-predictions.json'],
        ['data/goldfish-predictions.html'])
    #  |__   |  |
    #  |  |  |  |
    #  |  I  |  |
    run(filter_in_complete_sequences,
        ['data/reactions-only-good.json'],
        ['data/reactions-only-complete.json'])
    #  |  O  |  |
    #  |  |  |  |
    #  |  I  |  |
    run(reactions_to_sequence_visualization,
        ['data/reactions-only-complete.json'],
        ['data/reactions-only-complete.html'])
    #  |     |  |
    #  |     |  |
    #  I     |  |
    run(reactions_to_markov_predictions,
        ['data/reactions-only-good.json'],
        ['data/markov-predictions.json'])
    #  O     |  |
    #  |__   |  |
    #  |  |  |  |
    #  I  |  |  |
    run(markov_predictions_to_visualization,
        ['data/markov-predictions.json'],
        ['data/markov-predictions.html'])
    #     |  |  |
    #     I  I  I
    run(combine_predictions_to_csv,
        ['data/categorical-predictions.json',
         'data/goldfish-predictions.json',
         'data/markov-predictions.json'],
        ['data/predictions.csv'])


if __name__ == '__main__':
    pipeline()
