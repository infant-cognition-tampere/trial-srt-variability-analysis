# -*- coding: utf-8 -*-
'''
Visualize statistics
'''
import gazelib
import numpy as np
import bokeh.plotting as plotting
from bokeh.charts import Bar, Histogram

def run(input_files, output_files):

    # Read reaction sequences
    stats = gazelib.io.load_json(input_files[0])

    # Collect figures here.
    figs = []


    # Sequence completeness distribution
    d = {
        'num saccades captured': stats['total']['completeness'],
        'sequences': [1] * len(stats['total']['completeness'])
    }
    p = Bar(d, agg='count', label='num saccades captured', values='sequences', color='black')
    figs.append(p)


    # Saccademodel MSE distribution
    mses = stats['total']['all_mses']
    d = { 'MSE': list(filter(lambda x: x < 0.1, mses)) }
    p = Histogram(d, bins=40, values='MSE', color='black')
    figs.append(p)


    # Visualization with bokeh. Combine figures in vertical layout.
    p = plotting.vplot(*figs)
    plotting.output_file(output_files[0],
                         'Saccadic reaction time variability')
    plotting.save(p)
