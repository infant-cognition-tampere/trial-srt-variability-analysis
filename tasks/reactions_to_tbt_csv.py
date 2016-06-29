# -*- coding: utf-8 -*-
'''
Reaction sequences to a matrix form for Jukka to compare
'''
import gazelib.io

def run(input_files, output_files):
    trial_sequs = gazelib.io.load_json(input_files[0])

    dl = []

    for sequence in trial_sequs:
        for trial in sequence:
            dl.append(trial)

    gazelib.io.write_dictlist_as_csv(output_files[0], dl)
