# -*- coding: utf-8 -*-
import gazelib
from gazelib.statistics.utils import arithmetic_mean
from .lib.categorical import Categorical
from .lib.utils import get_srt_statistics, get_sequences_per_participant, get_participant_id

def run(input_files, output_files):

    # Read reaction sequences
    sequs = gazelib.io.load_json(input_files[0])

    valid = 'heuristic_saccade_validity'

    def get_predictions(sequences):
        prob_srts = []
        impr_srts = []

        # Let predictor perceive the sequences
        for sequence in sequences:
            # Create predictor.
            # Initialize one Categorical for each trial sequence.
            pred = Categorical()

            for trial in sequence:

                srt = trial['srt']
                stim_location = str(trial['stim_location'])

                # After we have seen each corner once.
                if pred.num_cats() >= 4:
                    if trial[valid]:
                        if stim_location in pred.nmode(2):
                            prob_srts.append(srt)
                        else:
                            impr_srts.append(srt)

                pred.learn(stim_location)

        return {
            'probable': {
                'srts': prob_srts,
                'stats': get_srt_statistics(prob_srts)
            },
            'improbable': {
                'srts': impr_srts,
                'stats': get_srt_statistics(impr_srts)
            }
        }

    per_participant = {}
    for par_sequences in get_sequences_per_participant(sequs):
        par_id = get_participant_id(par_sequences)
        preds = get_predictions(par_sequences)
        per_participant[par_id] = preds

    # Save as json
    data = {
        'total': get_predictions(sequs),
        'per_participant': per_participant
    }
    gazelib.io.write_json(output_files[0], data, human_readable=True)
