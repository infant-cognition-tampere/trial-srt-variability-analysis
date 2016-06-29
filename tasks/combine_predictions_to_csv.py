# -*- coding: utf-8 -*-
'''
Combine participant-wise analysis results to a matrix form for Jukka
analyze further.
'''
import gazelib.io

def run(input_files, output_files):
    hypotheses = {
        'categorical': gazelib.io.load_json(input_files[0]),
        'goldfish': gazelib.io.load_json(input_files[1]),
        'markov': gazelib.io.load_json(input_files[2])
    }

    rows = []

    for hyp_name, hyp in hypotheses.items():
        for par, conds in hyp['per_participant'].items():
            for condition, res in conds.items():
                s = res['stats']
                a = {
                    'participant_id': par,
                    'hypothesis': hyp_name,
                    'condition': condition,
                    'n': s['n'],
                    'inv_mean': s['inv_mean'],
                    'inv_std': s['inv_std'],
                    'inv_mean_ci68_lower': s['inv_mean_ci68'][0],
                    'inv_mean_ci68_upper': s['inv_mean_ci68'][1],
                    'inv_mean_ci95_lower': s['inv_mean_ci95'][0],
                    'inv_mean_ci95_upper': s['inv_mean_ci95'][1],
                    'mean': s['mean'],
                    'mean_ci68_lower': s['mean_ci68'][0],
                    'mean_ci68_upper': s['mean_ci68'][1],
                    'mean_ci95_lower': s['mean_ci95'][0],
                    'mean_ci95_upper': s['mean_ci95'][1]
                }
                rows.append(a)

    # Define column order
    headers = [
        'participant_id',
        'hypothesis',
        'condition',
        'n',
        'inv_mean',
        'inv_std',
        'inv_mean_ci68_lower',
        'inv_mean_ci68_upper',
        'inv_mean_ci95_lower',
        'inv_mean_ci95_upper',
        'mean',
        'mean_ci68_lower',
        'mean_ci68_upper',
        'mean_ci95_lower',
        'mean_ci95_upper'
    ]

    gazelib.io.write_dictlist_as_csv(output_files[0], rows, headers=headers)
