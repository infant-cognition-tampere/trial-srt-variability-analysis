
import gazelib
import numpy as np
import scipy as sp

def iter_sequence_files(input_files):
    for source_path in input_files:
        yield gazelib.containers.CommonV1(source_path)

def iter_target_periods(c):
    '''Parameters: c: CommonV1 object'''
    try:
        targets = c.iter_slices_by_tag('icl/experiment/reaction/period/target')
    except gazelib.containers.CommonV1.MissingTagException:
        # Skip empty and return empty generator
        # See http://stackoverflow.com/a/13243870/638546
        return

    for index, tgt in enumerate(targets):
        print('Target period #' + str(index).zfill(2))
        yield tgt.slice_first_microseconds(1000000)

def is_valid_saccade(srt, duration, mse):
    '''True if saccade is valid'''
    dur = duration
    return (100000 < srt and srt < 800000 and
            10000 < dur and dur < 80000 and
            mse < 0.05)

def to_milliseconds(srt):
    return round(srt / 1000)

def get_srt_statistics(srts):
    # 1 / SRT is normally distributed
    n = len(srts)

    if n <= 0:
        return {
            'n': n,
            'mean': None,
            'inv_mean': None,
            'inv_std': None,
            'inv_mean_ci95': [None, None],
            'inv_mean_ci68': [None, None],
            'mean_ci95': [None, None],
            'mean_ci68': [None, None]
        }

    inv_srts = [1 / t for t in srts]
    inv_mean = np.mean(inv_srts)
    mean = 1 / inv_mean

    if n <= 1:
        return {
            'n': n,
            'mean': mean,
            'inv_mean': inv_mean,
            'inv_std': None,
            'inv_mean_ci95': [None, None],
            'inv_mean_ci68': [None, None],
            'mean_ci95': [None, None],
            'mean_ci68': [None, None]
        }

    inv_sigma = np.std(inv_srts)
    inv_interval_scale = inv_sigma / np.sqrt(n)
    inv_interval = sp.stats.norm.interval(0.95, loc=inv_mean,
                                          scale=inv_interval_scale)
    inv_interv68 = sp.stats.norm.interval(0.68, loc=inv_mean,
                                          scale=inv_interval_scale)
    inv_interval = list(inv_interval)
    inv_interv68 = list(inv_interv68)
    interval = list(reversed([1 / t for t in inv_interval]))
    interv68 = list(reversed([1 / t for t in inv_interv68]))

    return {
        'n': len(srts),
        'mean': mean,
        'inv_mean': inv_mean,
        'inv_std': inv_sigma,
        'inv_mean_ci95': inv_interval,
        'inv_mean_ci68': inv_interv68,
        'mean_ci95': interval,
        'mean_ci68': interv68
    }

def get_participant_id(sequences):
    '''
    Get first participant ID from a list of sequences
    '''
    first_seq = sequences[0]
    first_trial = first_seq[0]
    return first_trial['head_id']

def get_sequences_per_participant(sequences):
    '''
    Return list (A) of list (B), where list (B) contains all trial sequences
    of single participant. This helps us to split the data for participant-wise
    analysis.
    '''

    def get_participant_id(sequence):
        first_trial = sequence[0]
        return first_trial['head_id']

    parts = {}
    for sequence in sequences:
        # Skip empty sequences. There has been at least one.
        if len(sequence) == 0:
            continue

        i = get_participant_id(sequence)

        if i in parts:
            parts[i].append(sequence)
        else:
            # Add first sequence
            parts[i] = [sequence]

    # Convert dict to list
    return list(parts.values())
