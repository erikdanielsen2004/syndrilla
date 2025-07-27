# Syndrilla
A PyTorch-based numerical simulator for decoders in quantum error correction.

<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/UnaryLab/syndrilla/main/images/qrcode_github.com.png" width="120">
    </td>
  </tr>
</table>

## Installation
All provided installation methods allow running ```syndrilla``` in the command line and ```import syndrilla``` as a python module.

Make sure you have [Anaconda](https://www.anaconda.com/) installed before the steps below.

### Option 1: pip installation
1. ```git clone``` [this repo](https://github.com/UnaryLab/syndrilla) and ```cd``` to the repo dir.
2. ```conda env create -f environment.yaml```
   - The ```name: syndrilla``` in ```evironment.yaml``` can be updated to a preferred one.
3. ```conda activate syndrilla```
4. ```pip install syndrilla```
5. Validate installation via ```syndrilla -h``` in the command line or ```import syndrilla``` in python code
   - If you want to validate the simulation results against BPOSD, you need to change python to version 3.10. Then install [BPOSD](https://github.com/quantumgizmos/bp_osd) and run ```python tests/validate_bposd.py```

### Option 2: source installation
This is the developer mode, where you can edit the source code with live changes reflected for simulation.
1. ```git clone``` [this repo](https://github.com/UnaryLab/syndrilla) and ```cd``` to the repo dir.
2. ```conda env create -f environment.yaml```
   - The ```name: syndrilla``` in ```evironment.yaml``` can be updated to a preferred one.
3. ```conda activate syndrilla```
4. ```python3 -m pip install -e . --no-deps```
5. Validate installation via ```syndrilla -h``` in the command line or ```import syndrilla``` in python code

## Basic Usage

### Run with command line arguments
Syndrilla simulation can be done via command-line arguments.
Below is an example command that runs a simulation using the BPOSD decoder:

```command
syndrilla -r=tests/test_outputs 
          -d=examples/alist/bposd_hz.decoder.yaml 
          -e=examples/alist/bsc.error.yaml 
          -c=examples/alist/lz.check.yaml 
          -s=examples/alist/perfect.syndrome.yaml 
          -bs=10000 
          -te=100
```

Following is a table for detailed explaination on each command line arguments:

| Argument | Description                                  | Example                                           |
|----------|----------------------------------------------|---------------------------------------------------|
| `-r`     | Path to store outputs                        | `-r=tests/test_outputs`                           |
| `-d`     | Path to decoder YAML file                    | `-d=examples/alist/bposd_hz.decoder.yaml`    |
| `-e`     | Path to error model YAML file                | `-e=examples/alist/bsc.error.yaml`                |
| `-c`     | Path to check matrix YAML file               | `-c=examples/alist/lz.check.yaml`                 |
| `-s`     | Path to syndrome extraction YAML file        | `-s=examples/alist/perfect.syndrome.yaml`         |
| `-ckpt`  | Path to checkpoint YAML file to resume | `-ch=result_phy_err.yaml`                         |
| `-bs`    | Number of samples in each batch             | `-bs=10000`                                       |
| `-te`    | Total number of errors to stop decoding      | `-te=100`                                         |
| `-l`     | Level of logger                              | `-l=SUCCESS`                                      |

### Output format and metrics
The result YAML file will be saved to the path specified by the ```-r``` option. 
In the example above, the result YAML file can be found in the ```tests/test_outputs``` folder.
This file includes both the metric results for each decoder and a summary of the full decoding.
Additionally, the result YAML file is updated every 100 batches, allowing Syndrilla to resume the simulation from the last checkpoint if the error budget was not reached in the previous run.

Example output of running above code:

```
decoder_0:
  algorithm: bp_norm_min_sum
  data qubit accuracy: 0.9993198895027624
  data qubit correction accuracy: 0.9351998631697068
  data frame error rate: 0.04856666666666667
  syndrome frame error rate: 0.04136666666666667
  logical error rate: 0.045033333333333335
  converge failure rate: 0.0036666666666666666
  converge success rate: 0.9549666666666666
  decoder invoke rate: 0.0
  average iteration: 6.650266666666667
  total time (s): '9.45191383361816406e-01'
  average time per batch (s): '3.15063794453938784e-01'
  average time per sample (s): '3.15063794453938808e-05'
  average time per iteration (s): '4.73096957769078096e-06'
decoder_1:
  algorithm: osd_0
  data qubit accuracy: 0.9993578268876612
  data qubit correction accuracy: 0.9372712592402529
  data frame error rate: 0.028999999999999998
  syndrome frame error rate: 0.0
  logical error rate: 0.004733333333333333
  converge failure rate: 0.004733333333333333
  converge success rate: 0.9952666666666666
  decoder invoke rate: 0.04136666666666666
  average iteration: 177.17491952736108
  total time (s): '9.68757629394531250e-01'
  average time per batch (s): '3.22919209798177065e-01'
  average time per sample (s): '3.22919209798177111e-05'
  average time per iteration (s): '1.82258306284528308e-07'
decoder_full:
  H matrix: /home/ya212494/code/syndrilla/examples/alist/surface/surface_10_hz.alist
  batch size: 10000
  batch count: 3
  target error: 100
  target error reached: 142
  physical error rate: 0.01
  logical error rate: 0.004733333333333333
  total time (s): '1.91394901275634766e+00'
```

Below tables will help user understand these metrics better.

Per-decoder metrics:
| Metric                           | Description                                                                 |
|----------------------------------|-----------------------------------------------------------------------------|
| `algorithm`                      | Name of the decoding algorithm used (e.g., `bp_norm_min_sum`, `osd_0`)      |
| `data qubit accuracy`            | Ratio of correctly matched data qubits over all data qubits                 |
| `data qubit correction accuracy` | Ratio of correctly identified data qubit errors                               |
| `data frame error rate`          | Ratio of samples with any data qubit mismatched                                |
| `syndrome frame error rate`      | Ratio of samples with any syndrome mismatche                                  |
| `logical error rate`             | Ratio of samples that have a logical error                               |
| `converge failure rate`          | Ratio of samples that successfully converge with a logical error  |
| `converge success rate`          | Ratio of samples that successfully converge without a logical error |
| `decoder invoke rate`            | Ratio of samples for which the decoder is invoked                           |
| `average iteration`              | Average number of iterations per sample                                    |
| `total time (s)`                 | Total time taken by the decoder in seconds                                  |
| `average time per batch (s)`     | Average time taken per batch in seconds                                     |
| `average time per sample (s)`    | Average time taken per sample in seconds                                    |
| `average time per iteration (s)` | Average time per iteration per sample in seconds                            |


Final metrics:
| Metric                         | Description                                                    |
|--------------------------------|----------------------------------------------------------------|
| `H matrix`                     | Path to the parity-check matrix used                           |
| `batch size`                   | Number of samples in each batch                               |
| `batch count`                  | Total number of batches                                    |
| `target error`                 | Total number of errors to stop decoding                        |
| `target error reached`         | Actual number of logical errors observed                       |
| `data type`                    | Floating point data used                                       |
| `physical error rate`          | Physical error rate                                            |
| `logical error rate`           | Logical error rate across all samples             |
| `total time (s)`               | Total simulation time across all batches in seconds            |

*Note that the time metric here only considers the decoding time.*

To change the configuration of the simulator, user need to update the YAML files. 
For example, if you want to use a different physical error rate, you need to find the input error YAML (e.g., ```examples/alist/bsc.error.yaml```) and update the ```rate``` field.

### Resume from checkpoint
If previous run is terminated by accident, the simulation can resume by setting the ```-ckpt``` to the checkpoint yaml file, the results of a previous run (e.g., ```tests/test_outputs=result_phy_err_0.01.yaml```).

```command
syndrilla -r=tests/test_outputs 
          -d=examples/alist/bposd_hz.decoder.yaml 
          -e=examples/alist/bsc.error.yaml 
          -c=examples/alist/lz.check.yaml 
          -s=examples/alist/perfect.syndrome.yaml 
          -bs=10000 
          -te=100
          -ckpt=tests/test_outputs=result_phy_err_0.01.yaml
```

### Sweeping configurations
Syndrilla also allows sweeping configurations during simulation, which is done in the ```zoo``` folder.
To generate all the configurations in the zoo directory, user can use the ```generate_sweeping_configs.py``` script. 

```command
python zoo/script/generate_sweeping_configs.py 
```

The configurations to sweep are specified in the ```sweeping_configs.yaml``` file.
It allows specifying decoder (decoder algorithm), code (code type), probability (physical error rate), check_type (check type), distance (code distance), and dtype (data type).
Below is an example:

```
decoder: [bposd, lottery_bposd]
code: [surface, toric]
probability: [0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.2, 0.5]
check_type: [hx, hz]
distance: [3, 5, 7, 9, 11, 13]
dtype: ['bfloat16', 'float16', 'float32', 'float64']
```

*Note that currently supported data format includes ['bfloat16', 'float16', 'float32', 'float64'].*

Once all configurations are prepared, you can see the corresponding folders in the ```zoo```, and you can now sweep the simulation using the ```run_sweeping.py``` script. 
This command will generate a corresponding result YAML file within each configuration folder.
Moreover, if a result YAML file already exists and simulation is terminated by accident, running the script again will, by default, automatically resume from the checkpoint, where the simulated is terminated.

```command
python zoo/script/run_sweeping.py -r=zoo/bposd_sweeping/ -d=bposd
```

There are command line arguments to control the script, allowing you to specify the configuration path, select the decoder, define batch sizes, and adjust logging verbosity.
| Argument | Description                                  | Example                                           |
|----------|----------------------------------------------|---------------------------------------------------|
| `-r`     | Path to configuration folder                 | `-r=zoo/bposd_sweeping/`                          |
| `-d`     | Decoder algorithm to run                     | `-d=bposd`                                        |
| `-bs`    | Number of samples run each batch             | `-bs=10000`                                       |
| `-l`     | Level of logger                              | `-l=SUCCESS`                                      |

## Simulation results
We show some of the simulation results as below.
These results show the impact of data format, code distance, physical error rate, and hardware on logical error rate and runtime.

GPUs: AMD Insticnt MI210, NVIDIA A100, NVIDIA H200

CPU: Intel i9-13900K

### Comparison across GPUs
<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/UnaryLab/syndrilla/main/zoo/speedup/accuracy_gpu.png" width="240"><br>Accuracy
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/UnaryLab/syndrilla/main/zoo/speedup/time_gpu.png" width="240"><br>Time
    </td>
  </tr>
</table>


### Comparison across data formats
<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/UnaryLab/syndrilla/main/zoo/speedup/accuracy_data_format.png" width="240"><br>Accuracy
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/UnaryLab/syndrilla/main/zoo/speedup/time_data_format.png" width="240"><br>Time
    </td>
  </tr>
</table>


### Comparison across distances
<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/UnaryLab/syndrilla/main/zoo/speedup/accuracy_distance.png" width="240"><br>Accuracy
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/UnaryLab/syndrilla/main/zoo/speedup/time_distance.png" width="240"><br>Time
    </td>
  </tr>
</table>


### Comparison across batch sizes and against CPU
<table>
  <tr>
    <td align="center">
      <img src="https://raw.githubusercontent.com/UnaryLab/syndrilla/main/zoo/speedup/time_batch.png" width="240"><br>Time
    </td>
    <td align="center">
      <img src="https://raw.githubusercontent.com/UnaryLab/syndrilla/main/zoo/speedup/time_cpu_speedup.png" width="240"><br>Speedup over CPU
    </td>
  </tr>
</table>


## Citation
If you use Syndrilla in your research, please cite the following paper:

```bibtex
@inproceedings{2025_qce_syndrilla,
	title={{Syndrilla: Simulating Decoders for Quantum Error Correction using PyTorch}},
	author={Yanzhang Zhu and Chen-Yu Peng and Yun Hao Chen and Siyuan Niu and Yeong-Luh Ueng and Di Wu},
	booktitle={International Conference on Quantum Computing and Engineering},
	year={2025}
} 
```

## Contribution
We warmly welcome contributions to Syndrilla — just open a pull request!
