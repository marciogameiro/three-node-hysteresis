#!/bin/bash

#SBATCH -J 3Node_Hyst         # Job name
#SBATCH -o output.%j.out      # stdout - %j expands to jobid
#SBATCH -e output.%j.err      # stderr - skip to combine stdout and stderr
#SBATCH -p normal             # Submit to the 'normal' or 'development' queue
#SBATCH -N 2                  # Number of nodes, not cores (stampeed2: 48 cores/node)
#SBATCH -n 96                 # Total number of tasks (if omitted, n=N)
#SBATCH -t 24:00:00           # Run time (hh:mm:ss)

# #SBATCH --mail-user=your_email
#SBATCH --mail-type=ALL

module load launcher

export LAUNCHER_PLUGIN_DIR=$LAUNCHER_DIR/plugins
export LAUNCHER_SCHED=dynamic
export LAUNCHER_RMI=SLURM

export LAUNCHER_WORKDIR=`pwd`
export LAUNCHER_JOB_FILE=jobfile.txt

$LAUNCHER_DIR/paramrun
 
$LAUNCHER_DIR/paramrun
