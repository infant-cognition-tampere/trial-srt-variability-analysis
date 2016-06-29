# -*- coding: utf-8 -*-
import gazelib
import bokeh.plotting as plotting
from bokeh.charts import Histogram

def run(input_files, output_files):
    '''Visualize predictions.json'''

    # Read prediction
    data = gazelib.io.load_json(input_files[0])
    same = data['total']['familiar']['srts']
    diff = data['total']['novel']['srts']

    # Collect figures here.
    figs = []

    d = {
        'SRT': same + diff,
        'group': ['Familiar' for x in same] + ['Novel' for x in diff]
    }
    p = Histogram(d, bins=10, values='SRT', color='group', legend='top_right')
    figs.append(p)

    # Visualization with bokeh. Combine figures in vertical layout.
    p = plotting.vplot(*figs)
    plotting.output_file(output_files[0],
                         'Saccadic reaction time variability')
    plotting.save(p)
