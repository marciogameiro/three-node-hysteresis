#!/bin/bash

mkdir -p ComputationsAscending

rm -f jobfile.txt

python3 CreateAscendingJobList.py > jobfile.txt

sbatch launcher_script.slurm
