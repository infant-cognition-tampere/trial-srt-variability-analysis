'''
This tasks does not yet fulfill the logic required for the pipeline.
It only provides a reference for proper implementation.

'''
import gazelib
import gazelib.conversion
import gazelib.visualization as gvis
import os
import re

def run(input_files, output_files):

    # Child Cognition file naming
    fileregexp = 'cg(\d+)_(\d+[a-z]?)_childcogn_(\d)m(NoCalib)?_SRT(\d)'
    p = re.compile(fileregexp)

    def recognizeName(fname):
        # Recognize metadata from filename
        bn = os.path.basename(fname)
        m = p.match(bn)
        return {
            'participant_id': m.group(1).zfill(4),
            'method_version': m.group(2),
            'participant_age_months': int(m.group(3)),
            'calibration_successful': (m.group(4) == None),
            'trial_configuration_id': 'SRT' + m.group(5)
        }

    convert = gazelib.conversion.icl.cg.common.convert

    source_dir = 'data/00_cg8mo-raw'
    target_dir = 'data/02_cg8mo-common'

    # Experiment configuration
    config_path = 'data/00_cg8mo-raw/cg_8_tbt-trial-config.json'

    # For each file in source_dir
    # 1. convert to gazelib/common/v1 and store as JSON

    def iter_first_target_seconds(commonv1):
        targets = c.iter_slices_by_tag('icl/experiment/reaction/period/target')
        for tgt in targets:
            yield tgt.slice_first_microseconds(1000000)

    for fpath in os.listdir(source_dir):
        if fpath.endswith(".gazedata"):
            source_path = os.path.join(source_dir, fpath)
            # Collect meta from filename
            meta = recognizeName(fpath)

            print('Converting participant ' + meta['participant_id'] +
                  ' trials ' + meta['trial_configuration_id'])
            c = convert(source_path, config_path,
                        meta['participant_id'],
                        meta['trial_configuration_id'],
                        meta['calibration_successful'])

            base, extension = os.path.splitext(fpath)
            base_name = os.path.basename(base)
            target_name = base_name + '.common.json'
            target_path = os.path.join(target_dir, target_name)
            c.save_as_json(target_path)
