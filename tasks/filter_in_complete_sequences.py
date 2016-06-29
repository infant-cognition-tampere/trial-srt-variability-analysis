# -*- coding: utf-8 -*-
'''
Filter out those sequences where at least one saccade is not valid.
'''
import gazelib

def run(input_files, output_files):
    # List of sequence lists
    sequences = gazelib.io.load_json(input_files[0])
    complete_sequences = []

    validity = 'heuristic_saccade_validity'

    for seq in sequences:
        if all([trial[validity] for trial in seq]):
            complete_sequences.append(seq)

    # For reference, print number of complete sequences
    print('# of sequences: ' + str(len(sequences)))
    print('# of complete sequences: ' + str(len(complete_sequences)))

    gazelib.io.write_json(output_files[0], complete_sequences,
                          human_readable=True)
