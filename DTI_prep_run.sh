#!/bin/bash

# To use DTIPrep, you need DWIConvert, which is now a part of Slicer. 
# https://github.com/Slicer/Slicer
# Ancient version available at:
# https://github.com/BRAINSia/BRAINSTools/tree/master/DWIConvert

if [ $# -eq 0 ]; then
echo "Usage: DTI_prep_mini.sh <data_dir> <subject_list.txt>. <data_dir> is subjects folder for FACT"
exit
fi

data_dir=$1
subject_list=$2

for sub in `cat ${subject_list}`; do

DWIConvert --inputDicomDirectory ${data_dir}/${sub} --outputVolume ${data_dir}/${sub}/${sub}.nrrd

echo "DTIPrep -w ${sub}.nrrd -c -d -p default.xml" | qsub -V -d ${data_dir}/${sub}/ -o ${data_dir}/${sub}/ -e ${data_dir}/${sub}/ -q max30

done
