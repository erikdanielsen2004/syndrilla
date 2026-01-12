import argparse
import os
import sys
import yaml
from pathlib import Path
from collections import OrderedDict

def main():
    parser = argparse.ArgumentParser(description='Prune results subfolders.')
    parser.add_argument('-r', '--run_dir', type=str, default=None, help='The directory whose subfolders should be pruned. Files other than result yaml files will be deleted.')
    args = parser.parse_args()
    base_path = Path(args.run_dir)

    for subfolder in sorted(base_path.iterdir()):
        if subfolder.is_dir():
            for subfile in sorted(subfolder.iterdir()):
                name = subfile.name
                if "result" not in name:
                    filepath = f'{base_path}/{subfolder.name}/{name}'
                    if (os.path.exists(filepath)):
                        os.remove(filepath)



    
