# Syndrilla
A PyTorch-based numerical simulator for decoders in quantum error correction.

## Installation
### Option 1: Standard installation
In the root directory, run following commands.
1. ```conda create --name syndrilla python```
2. ```conda activate syndrilla```
3. ```conda install -c conda-forge pyyaml yamlordereddictloader pytest loguru numpy scipy pynvml```
4. Install [PyTorch 2.x](https://pytorch.org/)
5. ```python3 -m pip install -e . --no-deps```
6. ```pytest``` to validate installation

### Option 2: Verifiable installation (with restricted python version)
In the root directory, run following commands.
1. ```conda create --name syndrilla python=3.10```
2. ```conda activate syndrilla```
3. ```conda install -c conda-forge pyyaml yamlordereddictloader pytest loguru numpy scipy pynvml```
4. Install [PyTorch 2.x](https://pytorch.org/).
5. ```python3 -m pip install -e . --no-deps```
6. ```pytest``` to validate installation
7. ```pip install -U bposd``` to install BPOSD
8. ```python tests/validate_bposd.py``` to validate against [BPOSD](https://github.com/quantumgizmos/bp_osd)

