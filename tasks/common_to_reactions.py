# -*- coding: utf-8 -*-
import gazelib.io
import gazelib.models as gmod
import os
from .lib.utils import iter_sequence_files, iter_target_periods, is_valid_saccade
from itertools import islice

# def to_ms(microseconds):
#     try:
#         return int(microseconds / 1000)
#     except:
#         return None



def get_reaction_sequences(input_files):
    '''
    Return a list of lists where the sublists are trial sequences
    '''
    reaction_sequences = []

    #for seq in islice(iter_sequence_files(input_files), 0, 2):
    for seq in iter_sequence_files(input_files):
        reaction_sequence = []
        for first_sec in iter_target_periods(seq):
            # Find saccade from that
            print('Fitting saccade model...')
            try:
                m = gmod.saccade.fit(first_sec)
            except:
                # Skip to next if somehow bad saccade.
                continue

            t_stim = first_sec.get_relative_start_time()
            t_reac = m['start_time_relative']
            t_stop = m['end_time_relative']

            srt = t_reac - t_stim
            dur = t_stop - t_reac
            mse = m['mean_squared_error']

            # Get stimulus location
            stim_event = first_sec.get_event_by_tag('icl/stimulus/image', 0)
            aoi_index_key = 'original_area_of_interest_index'
            stim_aoi_index = stim_event['extra'][aoi_index_key]

            # Get trial sequence number
            tag = 'icl/experiment/reaction/trial'
            trial_event = first_sec.get_event_by_tag(tag)
            extra_tag = 'icl/experiment/reaction/trial/sequence_number'
            trial_number = trial_event['extra'][extra_tag]

            # Get participant number
            env_name = 'gazelib/gaze/head_id'
            head_id = first_sec.get_environment(env_name)

            # Trial configuration
            env_name = 'icl/gaze/trial_configuration_id'
            trial_config_id = first_sec.get_environment(env_name)

            # Calibration success
            env_name = 'icl/gaze/tracker_successfully_calibrated'
            calibrated_bool = first_sec.get_environment(env_name)

            # Get source gazedata file name
            source_key = 'gazelib/general/source_files'
            source_file = seq.get_environment(source_key)[0]

            # Count number of nones and non-nones
            none_sum = 0
            nonone_sum = 0
            for stream_name in first_sec.list_stream_names():
                stream = first_sec.get_stream_values(stream_name)
                stream_none_sum = stream.count(None)
                none_sum += stream_none_sum
                nonone_sum += len(stream) - stream_none_sum

            # A heuristic for saccade validity
            line_saccade_validity = is_valid_saccade(srt, dur, mse)

            saccade = {
                'duration': dur,
                'head_id': head_id,
                'srt': srt,
                'mse': mse,
                'source': source_file,
                'trial_configuration_id': trial_config_id,
                'tracker_successfully_calibrated': calibrated_bool,
                'trial_number': trial_number,
                'stim_location': stim_aoi_index,
                'invalid_points': none_sum,
                'valid_points': nonone_sum,
                'heuristic_saccade_validity': line_saccade_validity
            }

            reaction_sequence.append(saccade)
        reaction_sequences.append(reaction_sequence)

    return reaction_sequences

def run(input_files, output_files):
    rs = get_reaction_sequences(input_files)
    gazelib.io.write_json(output_files[0], rs, human_readable=True)
