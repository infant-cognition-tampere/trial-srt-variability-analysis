# -*- coding: utf-8 -*-
'''
Visualize statistics
'''
import gazelib
import bokeh.plotting as plotting
from bokeh.charts import Bar, Histogram
from .lib.utils import to_milliseconds

def run(input_files, output_files):

    # Read reaction sequences
    sequs = gazelib.io.load_json(input_files[0])

    # Collect figures here.
    figs = []

    for sequence in sequs:

        srts = []

        # Trials
        for trial in sequence:
            if trial['heuristic_saccade_validity']:
                srts.append(trial['srt'])
            else:
                srts.append(0)

        # To milliseconds
        srts = list(map(to_milliseconds, srts))

        d = {
            'SRT': srts,
            'Trial': list(range(1,13))
        }
        p = Bar(d, label='Trial', values='SRT', color='black')
        figs.append(p)

    # Visualization with bokeh. Combine figures in vertical layout.
    p = plotting.vplot(*figs)
    plotting.output_file(output_files[0],
                         'Saccadic reaction time variability')
    plotting.save(p)
