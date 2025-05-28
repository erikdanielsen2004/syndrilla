import yaml
import subprocess
import re
import csv
import os
import shutil


def main():
    base_dir = "zoo/bp_sweeping"
    subdirs = sorted([d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d))])

    for subdir in subdirs:
        print(f"\n=== folder {subdir} ===")
        # checking whether the decoder is hx or hz
        folder_path = os.path.join(base_dir, subdir)
        if 'hx' in subdir:
            decoder_yaml = os.path.join(folder_path, "bp_hx.decoder.yaml")
            check_yaml = os.path.join(folder_path, "lx.check.yaml")
        else: 
            decoder_yaml = os.path.join(folder_path, "bp_hz.decoder.yaml")
            check_yaml = os.path.join(folder_path, "lz.check.yaml")

        error_yaml = os.path.join(folder_path, "bsc.error.yaml")
        syndrome_yaml = os.path.join(folder_path, "perfect.syndrome.yaml")

        # set command line arguement to load all yaml file from the folder
        cmd = [
            "syndrilla",
            f"-r={folder_path}/",
            f"-d={decoder_yaml}",
            f"-e={error_yaml}",
            f"-c={check_yaml}",
            f"-s={syndrome_yaml}",
            "-bs=100000",
            "-ss=1000000"
            "-o=examples/alist/output.yaml"
        ]

        print("Command: ", " ".join(cmd))
        result = subprocess.run(cmd, capture_output=True, text=True)

        # Print stdout/stderr for debugging
        print("  --> STDOUT:\n", result.stdout)
        print("  --> STDERR:\n", result.stderr)


if __name__ == "__main__":
    main()