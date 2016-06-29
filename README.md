# ICL Saccadic reaction time variability analysis

This program implements the analysis pipeline for an ICL project. The project examines how human memory can affect saccadic reaction times. The results are reported in a separate research report *Effects of memory to variation of saccadic reaction times of infants* by Akseli Palén and Jukka Leppänen.

The steps of the pipeline are defined under directory `tasks/` and written in Python. The source data, intermediate results, and the final results are stored under directory `data/`. The pipeline is defined and visually presented in the Python script `pipeline.py`.

## Setup

Conda is not necessary but gives convenient environment handling. Dependencies include `gazelib`, `numpy`, and `scipy`:

    $ conda create --name variability python=3
    $ source activate variability
    (variability)$ pip install gazelib

## Execute

Run analysis pipeline by:

    $ source activate variability
    (variability)$ python pipeline.py

The results of each step are cached under `data/` so their unnecessary computation can be skipped. The following tip reveals the caching logic: to force single computation of a step, modify the script of the step or remove or modify one of the input files.

If a file close to the pipeline root is modified, it might require a couple of runs before the change reaches the leaf steps. The pipeline logic needed to prevent this remains to be implemented.

## Author

Akseli Palén, akseli.palen@gmail.com

## License

The pipeline is released under MIT license.

The results and the source data under `data/` are property of Infant Cognition Laboratory at University of Tampere. Contact Jukka Leppänen (jukka.leppanen@staff.uta.fi) for further permissions.
