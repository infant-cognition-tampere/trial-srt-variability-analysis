# -*- coding: utf-8 -*-
'''
Anonymize reactions: randomize participant ids so that they do not match
the ids of the source data.
'''
import gazelib
import random

def run(input_files, output_files):

    # Read reaction sequences
    seqs = gazelib.io.load_json(input_files[0])

    # Generate 100 random participant ids and
    # consume them, one per participant. This way we avoid
    # overlapping ids. Still, ensure that the sequence remains the same
    # between runs by seeding the generator.
    random.seed(420)
    new_ids = list(map(lambda x: str(x).zfill(4), range(100,200)))
    random.shuffle(new_ids)

    # Mapping from head_id to new id. If head_id is faced after generating
    # iteration, we do not generate a new one but use the one stored here.
    head_id_to_new_id = {}

    for seq in seqs:
        if len(seq) > 0:
            head_id = seq[0]['head_id']

            if head_id in head_id_to_new_id:
                new_id = head_id_to_new_id[head_id]
            else:
                # Get new id
                new_id = new_ids.pop(0)
                head_id_to_new_id[head_id] = new_id

            # Overwrite true participant ids
            for trial in seq:
                trial['head_id'] = new_id

    gazelib.io.write_json(output_files[0], seqs, human_readable=True)
