#!/bin/bash
# a name for this job; letters and digits only please. (optional)
#SBATCH --job-name=cahoopes_python

# Researchers can buy in for priority queueing. However, the amount of time 
# they can use for this is limited.  Everyone has access to unlimited
# windfall, but any priority jobs will go first.  The partitions (queues) on
# Puma are windfall, standard, and high_pri
# non-windfall partitions require a "#SBATCH --account=your_PI_group line"
#SBATCH --partition=standard
#SBATCH --account=lecondon

# Standard Puma Nodes have 94 available cores and 480GB of available RAM each.
# Since no memory allocation is set, the ram available will be 5GB per core
# (Task in Sluem).
# Note: the fewer resources you request, the less time your job will spend in
# waiting and the more resources will be available for others to use.
#SBATCH --nodes=1
#SBATCH --ntasks=1

# This is the amount of time you think your job will take to run.
# 240 houra (10 days) is the maximum.
# This request shows 5 minutes
#SBATCH --time=00:05:00

# Reset modules, so we have a known starting point...
# module purge
# module load autotools prun/1.3 gnu8/8.3.0 openmpi3/3.1.4 ohpc
# module list

module load python/3.8
source ~/cahooopespyenv/bin/activate

# This will show which node your job is running on.
echo "This job is running on node `uname -n`"

# this will use some SLURM environment variables to tell a bit more about
# this job...
echo "This job is allocated ${SLURM_JOB_NUM_NODES} node(s), ${SLURM_JOB_CPUS_PER_NODE} core(s)/node and $((${SLURM_MEM_PER_CPU} / 1024 * ${SLURM_JOB_CPUS_PER_NODE})) Gigabytes of memory"

# *** If you need assistance using Puma, please email
# *** hpc-consult@list.arizona.edu

cd /home/u9/cahoopes/HASTools
python Hoopes_HW15.py

exit 0
#
#-end of puma_cpu sample script.

