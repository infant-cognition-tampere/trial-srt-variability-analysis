# -*- coding: utf-8 -*-
'''
Goldfish predictions:
    Predict next only from the previous stimulus location

Possible bias:
    General orientation speeds up the reaction times. Same locations are not
    possible on the first trial where relatively slow reaction times are common.

    Countermeasure: Do not count the first saccade.

'''
import gazelib
from gazelib.statistics.utils import arithmetic_mean
from .lib.categorical import Categorical
from .lib.utils import get_srt_statistics, get_sequences_per_participant, get_participant_id

def run(input_files, output_files):

    # Read reaction sequences
    sequs = gazelib.io.load_json(input_files[0])

    def get_predictions(sequences):
        same_srts = []
        diff_srts = []
        # same_fast = 0
        # same_slow = 0
        # diff_fast = 0
        # diff_slow = 0

        valid = 'heuristic_saccade_validity'

        for sequence in sequences:
            # Know the previous location
            # If saccade valid
            #   If location same:
            #     add srt to same_srts
            #   If location diff:
            #     add srt to diff_srts

            previous_location = 'none'

            # Bias countermeasure, see above.
            first = True

            for trial in sequence:

                stim_location = str(trial['stim_location'])

                if trial[valid] and not first:
                    if previous_location == stim_location:
                        same_srts.append(trial['srt'])
                    else:
                        diff_srts.append(trial['srt'])

                first = False
                previous_location = stim_location

        same_stat = get_srt_statistics(same_srts)
        diff_stat = get_srt_statistics(diff_srts)

        return {
            'same_location': {
                'srts': same_srts,
                'stats': same_stat
            },
            'diff_location': {
                'srts': diff_srts,
                'stats': diff_stat
            }
        }

    per_participant = {}
    for par_sequences in get_sequences_per_participant(sequs):
        par_id = get_participant_id(par_sequences)
        preds = get_predictions(par_sequences)
        per_participant[par_id] = preds

    data = {
        'total': get_predictions(sequs),
        'per_participant': per_participant
    }
    gazelib.io.write_json(output_files[0], data, human_readable=True)
