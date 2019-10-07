#!/bin/bash
#Active comments for SGE
#$ -V
#$ -cwd
#$ -j y
#$ -S /bin/bash
#$ -pe orte 1

#Active comments for SLURM
#SBATCH -n 1                 # One task
#SBATCH -c 1                 # One cpu per task
#SBATCH -N 1                 # Minimum one node
#SBATCH -t 1-00:00           # Runtime in D-HH:MM
#SBATCH -p main              # Partition to submit to
#SBATCH --mem-per-cpu=4000   # Memory pool for all cores (see also --mem-per-cpu)

# $1 Python script to run
# $2 output_folder
# $3 network_specification_file
# $4 starting_rpi
# $5 ending_rpi
# $6 gene (name) on which to do factor graph query
# $7 gene (name) which is on when in proliferative FP and off in quiescent FP

A=$2
B=`basename $3`
echo $A
echo "python3 $1 $3 ${A}/${B}_partial_hysteresis_$4_$5.txt ${A}/${B}_full_hysteresis_$4_$5.txt $4 $5 $6 $7"
python3 $1 $3 ${A}/${B}_partial_hysteresis_$4_$5.txt ${A}/${B}_full_hysteresis_$4_$5.txt $4 $5 $6 $7
# echo "python3 $1 $3 ${A}/${B}_partial_hysteresis_$4_$5.txt ${A}/${B}_partial_resettable_$4_$5.txt ${A}/${B}_full_hysteresis_$4_$5.txt ${A}/${B}_full_resettable_$4_$5.txt $4 $5 $6 $7"
# python3 $1 $3 ${A}/${B}_partial_hysteresis_$4_$5.txt ${A}/${B}_partial_resettable_$4_$5.txt ${A}/${B}_full_hysteresis_$4_$5.txt ${A}/${B}_full_resettable_$4_$5.txt $4 $5 $6 $7
