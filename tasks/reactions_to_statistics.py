# -*- coding: utf-8 -*-
'''
General statistics
'''
import gazelib
from gazelib.statistics.utils import arithmetic_mean
from .lib.categorical import Categorical
from .lib.utils import get_srt_statistics, get_sequences_per_participant

def run(input_files, output_files):

    # Read reaction sequences
    sequs = gazelib.io.load_json(input_files[0])

    def get_stats(sequences):
        num_invalid = 0
        num_valid = 0
        num_complete = 0
        num_incomplete = 0

        num_participants = 0
        participant_ids = []

        # Number of valid saccades per sequence
        sequence_completeness = []

        valid_srts = []
        valid_mses = []
        all_srts = []
        all_mses = []

        valid = 'heuristic_saccade_validity'

        for sequence in sequences:
            complete_sequence = True
            completeness = 0
            for trial in sequence:
                if trial[valid]:
                    num_valid += 1
                    completeness += 1
                    valid_srts.append(trial['srt'])
                    valid_mses.append(trial['mse'])
                else:
                    num_invalid += 1
                    complete_sequence = False
                all_srts.append(trial['srt'])
                all_mses.append(trial['mse'])
            if complete_sequence:
                num_complete += 1
            else:
                num_incomplete += 1
            sequence_completeness.append(completeness)
            if len(sequence) > 0:
                head_id = sequence[0]['head_id']
                if head_id not in participant_ids:
                    num_participants += 1
                    participant_ids.append(head_id)

        # Save as json
        return {
            'valid_srts_stats': get_srt_statistics(valid_srts),
            'valid_srts': valid_srts,
            'valid_mses': valid_mses,
            'all_srts': all_srts,
            'all_mses': all_mses,
            'num_valid': num_valid,
            'num_invalid': num_invalid,
            'num_total': num_valid + num_invalid,
            'num_complete_sequences': num_complete,
            'num_incomplete_sequences': num_incomplete,
            'num_sequences': num_complete + num_incomplete,
            'completeness': sequence_completeness,
            'num_participants': num_participants,
            'participant_ids': participant_ids
        }

    data = {
        'total': get_stats(sequs),
        'per_participant': {}
    }

    for participant_sequences in get_sequences_per_participant(sequs):
        stats = get_stats(participant_sequences)
        assert len(stats['participant_ids']) == 1
        par_id = stats['participant_ids'][0]
        data['per_participant'][par_id] = stats

    gazelib.io.write_json(output_files[0], data, human_readable=True)
