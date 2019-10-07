#!/bin/bash

# Command Line Arguments:
#   Argument 1 (optional): job submission command (e.g. qsub). Can be left blank.

mkdir -p ComputationsAscending

for filename in `ls Networks`; do
  python3 ../QueryScripts/EnqueueAscending.py ComputationsAscending Networks/${filename} X0 X2 $1
done
