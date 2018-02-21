#!/bin/bash
TBSS_DIR=$OM_HOME/tbss/tbss-dti-tk
THRESH=0.2
echo $TBSS_DIR
echo $THRESH

cd $TBSS_DIR

# tbss_4_prestats $THRESH

cd  $OM_HOME/scripts

python ./tbss-stats.py --tbss-directory $TBSS_DIR

if [ $? -ne 0 ]; then
    echo "Error in python file"
    exit 1
fi

cd $TBSS_DIR/stats

randomise -i all_FA_skeletonised -o tbss -m mean_FA_skeleton_mask \
    -d design.mat -t design.con -n 5000 --T2
