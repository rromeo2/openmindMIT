from scipy import stats
from sklearn import linear_model
import os
import sys
import json
import math
# import statsmodels.formula.api as sm
import numpy as np
# import statsmodels.sandbox.stats.multicomp as multcomp
import pandas as pd

om_home = "/om/user/jsegaran/"
behavioral_data = "./behavioral_data.json"
lena_data = "./lena_data.json"
# time_two = "./time_two.json"
subjects_file = "subjects.txt"
motion_file = "motion.txt"
lh_ilf_data = "lh.ilf.json"
vox_data_loc = "./vox-data/"
lh_slfp_voxel_data = "lh.slfp_PP.avg33_mni_bbr.FA_Avg.txt"
lh_slft_voxel_data = "lh.slft_PP.avg33_mni_bbr.FA_Avg.txt"
lh_slft_data = "lh.slft.json"
lh_slfp_data = "lh.slfp.json"
FA_points = False
is_run_local = False

def regress_out(x, y):
    reg = linear_model.LinearRegression()
    x_data = np.array(x).astype(np.float)
    y_data = np.array(y).astype(np.float)
    reg.fit(x_data, y_data)
    reg.coef_

    final_y = []
    for i in range(len(x_data)):
        subj = subjects[i]
        predicted = reg.predict([x_data[i]])
        final_y.append(y_data[i]-predicted[0])
    return final_y

if __name__ == "__main__":

    cwd = os.getcwd()

    for i in range(len(sys.argv)):
        arg = sys.argv[i]

        if arg == "--tbss-directory":
            tbss_directory = sys.argv[i+1]


        if arg == "--xyz":
            FA_points = True
            xyz = sys.argv[i+1]
            x = xyz.split(",")[0]
            y = xyz.split(",")[1]
            z = xyz.split(",")[2]

        if arg == "--mask":
            FA_points = True
            mask = True
            mask_file = sys.argv[i+1]

        if arg == "-o" or arg == "--output":
            output_file = sys.argv[i+1]

        if arg == "--local":
            is_run_local = True
            import matplotlib.pyplot as plt
            import time
            om_home = "/home/joshua/UROP/OM_HOME/"

    # tbss_directory = om_home + "/tbss/tbss-tracula-CTC"
    # data_dir = om_home + "scripts/data"

    # os.chdir(data_dir)

    file = open(behavioral_data, 'r')
    behav_data = json.load(file)
    file.close()

    file = open(lena_data, 'r')
    lena_data = json.load(file)
    file.close()

    # file = open(time_two, 'r')
    # time_two = json.load(file)
    # file.close()

    # file = open(lh_ilf_data, 'r')
    # lh_ilf_data = json.load(file)
    # file.close()

    # file = open(lh_slft_data, 'r')
    # lh_slft_data = json.load(file)
    # file.close()

    # file = open(lh_slfp_data, 'r')
    # lh_slfp_data = json.load(file)
    # file.close()

    # os.chdir(vox_data_loc)
    lh_slfp_voxel_data = pd.DataFrame.from_csv(lh_slfp_voxel_data, header=0,
            sep=" ", index_col=-1)
    for i in lh_slfp_voxel_data.keys():
        if "FACT" not in i:
            del lh_slfp_voxel_data[i]

    lh_slft_voxel_data = pd.DataFrame.from_csv(lh_slft_voxel_data, header=0,
            sep=" ",index_col=-1)
    for i in lh_slft_voxel_data.keys():
        if "FACT" not in i:
            del lh_slft_voxel_data[i]
    # os.chdir(tbss_directory)

    file = open(subjects_file, 'r')
    subjects = sorted(json.load(file))
    file.close()

    file = open(motion_file, 'r')
    total_motion_index = json.load(file)
    file.close()

    # os.chdir("./stats")
    # if FA_points:
    #     if not mask:
    #         points_text = subprocess.check_output(["fslmeants", "-i",
    #             "all_FA_skeletonised.nii.gz", "-c", str(x), str(y), str(z)])
    #     else:
    #         points_text = subprocess.check_output(["fslmeants", "-i",
    #             "all_FA_skeletonised.nii.gz", "-m", str(mask_file)])
    #     points = points_text.split("\n")
    # if not FA_points:
    #     points = ['0'] * len(subjects)

    # os.chdir(cwd)


    high_SES = behav_data['mom_college']
    mom_ed = behav_data['mom_ed']
    parent = behav_data['mom_ed']

    AWC = lena_data['AWC']
    CVC = lena_data['CVC']
    CTC = lena_data['CTC']
    mean_verbal = behav_data['PPVT_std_T1']
    comb_SES = behav_data['SES_avg_parentEdIncome_z']
    age = behav_data['age']
    gender = behav_data['sex']

    # lh_ilf_FA_Avg = lh_ilf_data["FA_Avg"]
    # lh_slfp_FA_Avg = lh_slfp_data["FA_Avg"]
    # lh_slft_FA_Avg = lh_slft_data["FA_Avg"]

    # lh_slft_Volume = lh_slft_data["Volume"]
    # lh_slfp_Volume = lh_slfp_data["Volume"]
    # lh_ilf_Volume = lh_ilf_data["Volume"]

    for j in range(len(lh_slfp_voxel_data['FACT_102'])):
        final_x = []
        x_data = []
        y_data = []
        other = []
        skip = False
        for i in range(len(subjects)):
            subj = subjects[i]
            if mean_verbal[subj] in '':
                continue

            if(math.isnan(float(lh_slfp_voxel_data[subj][j]))):
                skip=True
            y_data.append(float(lh_slfp_voxel_data[subj][j]))
            x_data.append([gender[subj], age[subj],
                str(total_motion_index[subj])])
            final_x.append(float(CTC[subj]))

        if skip:
            continue
        final_y = y_data
        slope, intercept, r_value, p_value, std_err = stats.linregress(final_x,
                final_y)

        print(p_value, j)



    # if is_run_local:
    #     fig, ax = plt.subplots()
    #     ax.plot(final_x, final_x*slope +intercept)
    #     ax.scatter(final_x, final_y)
    #     fig.show()

    # data = {}
    # data['fa'] = []
    # data['high_ses'] = []
    # data['CTC'] = []
    # for i in range(len(subjects)):
    #     data['fa'].append(final_y[i])
    #     data['high_ses'].append(int(high_SES[subjects[i]]))
    #     data['CTC'].append(int(CTC[subjects[i]]))
    # data['high_ses'] = np.choose(data['high_ses'], ['low', 'high'])
    # result = sm.ols(formula='fa ~ CTC + high_ses
