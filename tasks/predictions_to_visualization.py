# -*- coding: utf-8 -*-
import gazelib
import bokeh.plotting as plotting
from bokeh.charts import Bar

def run(input_files, output_files):
    '''Visualize predictions.json'''

    # Read prediction sequences
    seq = gazelib.io.load_json(input_files[0])
    durs = seq['dur']
    srts = seq['srt']
    probs = seq['prob']

    # Collect figures here.
    figs = []

    # Prob vs SRT
    p = plotting.figure(title='Machine prediction vs measured reaction time',
                        x_axis_label='Predicted probability',
                        y_axis_label='Normalized saccadic reaction time',
                        plot_width=800, plot_height=800)
    p.cross(probs, srts, size=8, line_color='black')
    figs.append(p)

    # Prob vs duration
    p = plotting.figure(title='Machine prediction vs measured duration',
                        x_axis_label='Predicted probability',
                        y_axis_label='Normalized saccade duration',
                        plot_width=800, plot_height=800)
    p.cross(probs, durs, size=8, line_color='black')
    figs.append(p)

    # SRT vs duration
    p = plotting.figure(title='Saccadic reaction time vs saccade duration',
                        x_axis_label='Normalized saccadic reaction time',
                        y_axis_label='Normalized saccade duration',
                        plot_width=800, plot_height=800)
    p.cross(srts, durs, size=8, line_color='black')
    figs.append(p)

    # Visualization with bokeh. Combine figures in vertical layout.
    p = plotting.vplot(*figs)
    plotting.output_file(output_files[0],
                         'Saccadic reaction time variability')
    plotting.save(p)
