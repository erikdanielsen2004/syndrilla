# Syndrilla
A PyTorch-based numerical simulator for decoders in quantum error correction.

## Installation
All provided installation methods allow running ```syndrilla``` in the command line and ```import syndrilla``` as a python module.

Make sure you have [Anaconda](https://www.anaconda.com/) installed before the steps below.

### Option 1: pip installation (python>=3.9)
1. ```conda create --name syndrilla python```
2. ```conda activate syndrilla```
3. ```pip install syndrilla```
4. validate installation via ```syndrilla -h``` in the command line or ```import syndrilla``` in python code

### Option 2: source installation
Before installation, .
In the root directory of the repo, run following commands.

*This is the developer mode, where you can edit the source code with live changes reflected in simulation.*
1. ```git clone``` [this repo](https://github.com/UNARY-Lab/syndrilla)
2. ```conda create --name syndrilla python```
3. ```conda activate syndrilla```
4. ```conda install -c conda-forge pyyaml yamlordereddictloader pytest loguru numpy scipy pyfiglet pynvml```
5. Install [PyTorch 2.x](https://pytorch.org/)
6. ```python3 -m pip install -e . --no-deps```
7. validate installation via ```syndrilla -h``` in the command line or ```import syndrilla``` in python code

*If you want to validate this execution against BPOSD, you need to change python to version 3.10. Then install [BPOSD](https://github.com/quantumgizmos/bp_osd) and run ```python tests/validate_bposd.py```*


