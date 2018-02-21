import os
import shutil
import sys
import json
import numpy as np
import pickle
from scipy.stats import iqr

def caculate_stats(avg_trans_map, avg_rot_map, perc_bad_slices, avg_drop_map):
    trans_list = np.array(avg_trans_map.values()).astype(np.float)
    trans_median = np.median(trans_list)
    trans_iqr = iqr(trans_list)

    rot_list = np.array(avg_rot_map.values()).astype(np.float)
    rot_median = np.median(rot_list)
    rot_iqr = iqr(rot_list)

    # perc_list = np.array(perc_bad_slices.values()).astype(np.float)
    # perc_median = np.median(perc_list)
    # perc_iqr = iqr(perc_list)

    # drop_list = np.array(avg_drop_map.values()).astype(np.float)
    # print drop_list
    # drop_median = np.median(drop_list)
    # drop_iqr = iqr(drop_list)


    total_motion_index = {}
    for key in avg_trans_map.keys():
        total_motion_index[key] = (float(avg_trans_map[key])-trans_median)/trans_iqr
        total_motion_index[key] += (float(avg_rot_map[key])-rot_median)/rot_iqr
        # total_motion_index[key] += (float(perc_bad_slices[key])-perc_median)/perc_iqr
        # total_motion_index[key] += (float(avg_drop_map[key])-drop_median)/drop_iqr

    return total_motion_index




if __name__ == "__main__":
    tracula_folder = "/om/project/FACT/analysis/tracula/"
    output = "/om/user/jsegaran/tbss-SES"

    include = ["FACT_104", "FACT_105", "FACT_106", "FACT_113", "FACT_115",
            "FACT_119", "FACT_123", "FACT_129", "FACT_142", "FACT_143",
            "FACT_147", "FACT_159", "FACT_161", "FACT_163", "FACT_165",
            "FACT_171", "FACT_172", "FACT_176", "FACT_177", "FACT_179",
            "FACT_180", "FACT_182", "FACT_110", "FACT_114", "FACT_122",
            "FACT_168", "FACT_174", "FACT_175", "FACT_120", "FACT_131",
            "FACT_151", "FACT_160"]

    no_ef_info = ["FACT_102"]

    bad = ["FACT_166", "FACT_116", "FACT_149", "FACT_128",
            "FACT_121", "FACT_167", "FACT_181", "FACT_140"]


    no_lena_info = ["FACT_108", "FACT_109", "FACT_132", "FACT_178", "FACT_155", "FACT_156"]
    
    atypical_subjs = ["FACT_126", "FACT_137", "FACT_138", "FACT_148", "FACT_157"]

    time_two = ["FACT_113", "FACT_114", "FACT_115", "FACT_116", "FACT_117",
            "FACT_118", "FACT_119", "FACT_120", "FACT_121", "FACT_122",
            "FACT_123", "FACT_124", "FACT_125", "FACT_126", "FACT_127",
            "FACT_128", "FACT_129", "FACT_130", "FACT_131", "FACT_132",
            "FACT_133", "FACT_134", "FACT_135", "FACT_136", "FACT_137",
            "FACT_138", "FACT_139", "FACT_140", "FACT_141", "FACT_142",
            "FACT_143", "FACT_144", "FACT_145", "FACT_146", "FACT_147",
            "FACT_148", "FACT_149", "FACT_150", "FACT_151", "FACT_152",
            "FACT_153", "FACT_154", "FACT_155", "FACT_156", "FACT_157",
            "FACT_158", "FACT_159", "FACT_160", "FACT_161", "FACT_162",
            "FACT_163", "FACT_164", "FACT_165", "FACT_166"]

    lena = False
    ef = False
    onlyGood = False
    time_two_also = False
    atypical = False
    remove = []

    avg_trans_map = {}
    avg_rot_map = {}
    perc_bad_slices = {}
    avg_drop_map = {}


    for i in range(len(sys.argv)):
        arg = sys.argv[i]
        if arg == "--lena":
            lena = True
            print "Not including children with no lena"

        if arg == "--ef":
            ef = True
            print "Not including children with no ef"

        if arg == "--good":
            onlyGood = True
            print "Only good subjs"

        if arg == "-o":
            output = sys.argv[i+1]

        if arg == "--t2":
            print "Only including subjects with time two also"
            time_two_also = True

        if arg == "--atypical":
            print "Adding atypical developement"
            atypical = True

        if arg == "--remove":
            remove.append(sys.argv[i+1])


    if not lena:
        include = no_lena_info + include

    if not ef:
        include = no_ef_info + include

    if not onlyGood:
       include = include + bad

    if atypical:
       include = include + atypical_subjs


    if time_two_also:
       include_copy = include[:]
       for subj in include_copy:
           if subj not in time_two:
               include.remove(subj)

    for rem in remove:
        if rem in include:
            include.remove(rem)

    print sorted(include), len(sorted(include))

    all_dirs = os.listdir(tracula_folder)
    os.mkdir(output)
    os.chdir(output)

    for dir in all_dirs:
        if dir in include:
          shutil.copyfile(tracula_folder+dir+"/dmri/mni/dtifit_FA.bbr.nii.gz", dir+"_FA.nii.gz")
          stats = open(tracula_folder+dir+"/dmri/dwi_motion.txt",
                  "r").read().splitlines()[1].split(" ")
          avg_trans_map[dir] = stats[0]
          avg_rot_map[dir] = stats[1]
          perc_bad_slices[dir] = stats[2]
          avg_drop_map[dir] = stats[3]

    f = open('subjects.txt', 'w')
    json.dump(sorted(include), f)
    f.close()

    total_motion_index = caculate_stats(avg_trans_map, avg_rot_map, perc_bad_slices, avg_drop_map)

    f = open('motion.txt', 'w')
    json.dump(total_motion_index, f)
    f.close()
