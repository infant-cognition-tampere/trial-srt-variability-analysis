# -*- coding: utf-8 -*-
'''
Filter out those sequences where at least 6 saccades are not valid.
'''
import gazelib

def run(input_files, output_files):
    # List of sequence lists
    sequences = gazelib.io.load_json(input_files[0])
    complete_sequences = []

    validity = 'heuristic_saccade_validity'

    for seq in sequences:
        num_valid = len([1 for trial in seq if trial[validity]])
        if num_valid > 6:
            complete_sequences.append(seq)

    # For reference, print number of complete sequences
    print('# of sequences: ' + str(len(sequences)))
    print('# of good (compl > 6) sequences: ' + str(len(complete_sequences)))

    gazelib.io.write_json(output_files[0], complete_sequences,
                          human_readable=True)
