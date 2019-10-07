#!/bin/bash

mkdir -p ComputationsDescending

rm -f jobfile.txt

python3 CreateDescendingJobList.py > jobfile.txt

sbatch launcher_script.slurm
