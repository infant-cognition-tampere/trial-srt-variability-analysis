# -*- coding: utf-8 -*-
import gazelib
import bokeh.plotting as plotting
from bokeh.charts import Bar, BoxPlot, Histogram
#import matplotlib.pyplot as plt

def run(input_files, output_files):
    '''Visualize predictions.json'''

    # Read prediction
    data = gazelib.io.load_json(input_files[0])
    #same = data['same_location']
    #diff = data['diff_location']
    same = data['total']['same_location']['srts']
    diff = data['total']['diff_location']['srts']

    # Collect figures here.
    figs = []

    # Reaction times
    # if 'same_location' in seq:
    #     d = {
    #         'Location': ['Same', 'Different'],
    #         'Median SRT': [seq['same_location']['median_srt'],
    #                        seq['diff_location']['median_srt']]
    #     }
    #     p = Bar(d, label='Location', values='Median SRT', title='')

    d = {
        'SRT': same + diff,
        'group': ['Same' for x in same] + ['Diff' for x in diff]
    }
    p = Histogram(d, bins=7, values='SRT', color='group')
    figs.append(p)

    # Visualization with bokeh. Combine figures in vertical layout.
    p = plotting.vplot(*figs)
    plotting.output_file(output_files[0],
                         'Saccadic reaction time variability')
    plotting.save(p)
