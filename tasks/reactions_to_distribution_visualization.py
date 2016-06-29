# -*- coding: utf-8 -*-
'''
Visualize reaction time distribution
'''
import gazelib
import numpy as np
import bokeh.plotting as plotting
from bokeh.charts import Bar

def run(input_files, output_files):

    # Read reaction sequences
    seqs = gazelib.io.load_json(input_files[0])

    # Collect figures here.
    figs = []

    # Visualize reaction times of only valid saccades
    valids = []
    for seq in seqs:
        for trial in seq:
            if trial['heuristic_saccade_validity']:
                valids.append(trial['srt'])

    hist, bin_edges = np.histogram(valids, 20)
    d = {
        'SRT': bin_edges.tolist()[:-1],
        'num': hist
    }
    p = Bar(d, label='SRT', values='num', title='')
    figs.append(p)

    # Probit plot
    inv_valids = [1/t for t in valids]
    hist, bin_edges = np.histogram(inv_valids, 20)
    edges = bin_edges.tolist()[:-1]
    d = {
        'SRT': [1/t for t in edges],
        'num': hist
    }
    p = Bar(d, label='SRT', values='num', title='')
    figs.append(p)

    # Visualization with bokeh. Combine figures in vertical layout.
    p = plotting.vplot(*figs)
    plotting.output_file(output_files[0],
                         'Saccadic reaction time distribution')
    plotting.save(p)
