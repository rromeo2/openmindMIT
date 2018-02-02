#!/bin/bash

# to submit:
# sbatch -t 2-00:00:00 --mem=10GB run-diffusion.sh

## add all the cudas to enviornment
module add netcdf/gcc/64/4.3.1.1
module add cuda55/toolkit/5.5.22
export LD_LIBRARY_PATH=/om/user/satra/projects/SAD/scripts/lib/:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=/om/user/ksitek/HCP/scripts/lib/:/cm/shared/apps/cuda55/toolkit/5.5.22/lib64:/cm/shared/apps/cuda55/toolkit/5.5.22/lib:/cm/shared/apps/cuda65/toolkit/6.5.14/lib64:$LD_LIBRARY_PATH
module add openmind/cuda/8.0

datadir=/om/project/FACT/subjects
fsdir=/mindhive/xnat/surfaces/FACT/

python Eddy_tracula_csd.py
