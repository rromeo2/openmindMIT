#!/bin/sh

mni=false

OUTPUT=$OM_HOME/tbss-tracula

python tbss-remake.py --good --lena -o $OUTPUT

if [ $? -ne 0 ]; then
    echo "Error in python file"
    exit 1
fi


cd $OUTPUT
tbss_1_preproc *.nii.gz

if [ "$mni" = true ]; then
    tbss_2_reg -T
else
    tbss_2_reg -n
fi

tbss_3_postreg -S
