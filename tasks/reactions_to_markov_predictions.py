# -*- coding: utf-8 -*-
'''
Markov predictions

Test:
    We want to test if repeated pairs of consecutive locations yield faster
    saccades.

Null hypothesis
    No difference in reaction time.

Another hypothesis
    Possible speedup is caused because the general orientation because
    familiar pairs are more probable on the later part.

    Countermeasure: do not count novel pairs until first familiar pair.
    Implication: number novel saccades drops from 1042 to 254
'''
import gazelib
from .lib.utils import get_srt_statistics, get_sequences_per_participant, get_participant_id

def run(input_files, output_files):

    def get_predictions(sequences):
        # Familiar = the consecutive corner combination is seen before
        # Novel = the combination not seen before
        familiar_srt = []
        novel_srt = []

        valid = 'heuristic_saccade_validity'

        for seq in sequences:

            # Previous consecutive pairs.
            # Transfers from corner to corner
            loc2loc = {}

            prev_loc = None

            # The countermeasure to prevent the impact of general orientation.
            familiar_pair_seen = False

            for trial in seq:
                loc = str(trial['stim_location'])
                srt = trial['srt']

                if prev_loc is not None:
                    # Consider only valid saccades
                    if trial[valid]:
                        # If this combination of prev_loc and loc previously seen
                        if prev_loc in loc2loc and loc2loc[prev_loc] == loc:
                            familiar_srt.append(srt)
                            familiar_pair_seen = True
                        elif familiar_pair_seen:
                            novel_srt.append(srt)

                    # Learn
                    loc2loc[prev_loc] = loc

                prev_loc = loc

        familiar_stat = get_srt_statistics(familiar_srt)
        novel_stat = get_srt_statistics(novel_srt)

        # Save as json
        return {
            'familiar': {
                'srts': familiar_srt,
                'stats': familiar_stat
            },
            'novel': {
                'srts': novel_srt,
                'stats': novel_stat
            }
        }

    # Read reaction sequences
    seqs = gazelib.io.load_json(input_files[0])

    per_participant = {}
    for par_sequences in get_sequences_per_participant(seqs):
        par_id = get_participant_id(par_sequences)
        preds = get_predictions(par_sequences)
        per_participant[par_id] = preds

    data = {
        'total': get_predictions(seqs),
        'per_participant': per_participant
    }

    gazelib.io.write_json(output_files[0], data, human_readable=True)
