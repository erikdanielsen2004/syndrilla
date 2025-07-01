# Syndrilla
A PyTorch-based numerical simulator for decoders in quantum error correction.

## Installation
Before installation, git clone this GitHub [repo](https://github.com/UNARY-Lab/syndrilla).
The installation methods bellow allows to run ```syndrilla``` both in the command line and import ```syndrilla``` as a python module.

### Option 1: pip installation (python>=3.9)
In the root directory of the repo, run following commands.
1. ```conda create --name syndrilla python```
2. ```conda activate syndrilla```
3. ```pip install syndrilla```
4. ```syndrilla -h``` and python ```import syndrilla``` to validate installation

### Option 2: source installation
In the root directory of the repo, run following commands.

*This is the developer mode, where you can edit the source code with live changes.*
1. ```conda create --name syndrilla python```
2. ```conda activate syndrilla```
3. ```conda install -c conda-forge pyyaml yamlordereddictloader pytest loguru numpy scipy pyfiglet pynvml```
4. Install [PyTorch 2.x](https://pytorch.org/)
5. ```python3 -m pip install -e . --no-deps```
6. ```syndrilla -h``` and python ```import syndrilla``` to validate installation

### Option 3: verifiable installation (with restricted python version)
In the root directory of the repo, run following commands.
1. ```conda create --name syndrilla python=3.10```
2. ```conda activate syndrilla```
3. ```conda install -c conda-forge pyyaml yamlordereddictloader pytest loguru numpy scipy pyfiglet pynvml```
4. Install [PyTorch 2.x](https://pytorch.org/)
5. ```python3 -m pip install -e . --no-deps```
6. ```syndrilla -h``` and python ```import syndrilla``` to validate installation
7. ```pip install -U bposd``` to install BPOSD
8. ```python tests/validate_bposd.py``` to validate against [BPOSD](https://github.com/quantumgizmos/bp_osd)

