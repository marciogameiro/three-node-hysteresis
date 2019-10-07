#!/bin/bash

# Command Line Arguments:
#   Argument 1 (optional): job submission command (e.g. qsub). Can be left blank.

mkdir -p ComputationsDescending

for filename in `ls Networks`; do
  python3 ../QueryScripts/EnqueueAscending.py ComputationsDescending Networks/${filename} X0 X2 $1
done
