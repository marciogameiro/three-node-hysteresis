#!/bin/bash

module load python3/3.7.0

mkdir -p Networks
python3 GenerateThreeNode.py

mv Networks ..
