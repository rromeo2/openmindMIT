from decimal import Decimal
import os
import sys
import json
import pickle
import subprocess

behavioral_data = "./behavioral_data.json"
lena_data = "./lena_data.json"
time_two = "./time_two.json"
tbss_directory = "/om/user/jsegaran/tbss/tbss-tracula-interaction"
subjects_file = "subjects.txt"
motion_file = "motion.txt"
dti_data = "dti.json"
lh_slft_data = "lh.slft.json"
lh_slfp_data = "lh.slfp.json"
lh_ilf_data = "lh.ilf.json"
unc_data = "lh.unc.json"
data_dir = "/om/user/jsegaran/scripts/data"
output_file = "test.dat"
mask = False
FA_points = False
mask_file = ""
x = 0
y = 0
z = 0

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


    os.chdir(data_dir)

    file = open(behavioral_data, 'r')
    behav_data = json.load(file)
    file.close()

    file = open(lena_data, 'r')
    lena_data = json.load(file)
    file.close()

    file = open(time_two, 'r')
    time_two = json.load(file)
    file.close()

    file = open(dti_data, 'r')
    dti_data = json.load(file)
    file.close()

    file = open(lh_slft_data, 'r')
    lh_slft_data = json.load(file)
    file.close()

    file = open(lh_slfp_data, 'r')
    lh_slfp_data = json.load(file)
    file.close()

    file = open(lh_ilf_data, 'r')
    lh_ilf_data = json.load(file)
    file.close()

    file = open(unc_data, 'r')
    unc_data = json.load(file)['FA_Avg']
    file.close()

    os.chdir(tbss_directory)
    file = open(subjects_file, 'r')
    subjects = sorted(json.load(file))
    file.close()

    file = open(motion_file, 'r')
    total_motion_index = json.load(file)
    file.close()

    os.chdir("./stats")
    if FA_points:
        if not mask:
            points_text = subprocess.check_output(["fslmeants", "-i",
                "all_FA_skeletonised.nii.gz", "-c", str(x), str(y), str(z)])
        else:
            points_text = subprocess.check_output(["fslmeants", "-i",
                "all_FA_skeletonised.nii.gz", "-m", str(mask_file)])
        points = points_text.split("\n")
    if not FA_points:
        points = ['0'] * len(subjects)

    os.chdir(cwd)


    high_SES = behav_data['mom_college']
    mom_ed = behav_data['mom_ed']
    CTC = lena_data['CTC']
    AWC = lena_data['AWC']
    comb_SES = behav_data['SES_avg_parentEdIncome_z']
    age = behav_data['age']
    gender = behav_data['sex']
    lh_ilf_FA_Avg = dti_data['lh_ilf_FA_regressed']
    lh_slfp_FA_Avg = dti_data['lh_slfp_FA_regressed']
    lh_slft_FA_Avg = dti_data['lh_slft_FA_regressed']
    lh_slft_Volume = lh_slft_data["Volume"]
    lh_slfp_Volume = lh_slfp_data["Volume"]
    lh_ilf_Volume = lh_ilf_data["Volume"]

    matrix_file = open(output_file, 'w')

    matrix_file.write("mom_ed comb_SES total_motion_index CTC FA " +
    "gender ilf_Vol slft_Vol slfp_Vol unc_data AWC High_SES\n")
    for i in range(len(subjects)):
        subj = subjects[i]
        if time_two["PPVTssChange"][subj] == "":
            time_two["PPVTssChange"][subj] = "-100"
            time_two["Intervention_Completed"][subj] = "-100"

        #1
        matrix_file.write(mom_ed[subj] + " ")
        #2
        matrix_file.write(comb_SES[subj] + " ")
        #3
        matrix_file.write(str(total_motion_index[subj]) + " ")
        #4
        matrix_file.write(CTC[subj] + " ")

        #5
        matrix_file.write(points[i] + " ")

        #8
        matrix_file.write(gender[subj] + " ")
        #9
        matrix_file.write(str(lh_ilf_Volume[subj]) + " ")
        #10
        matrix_file.write(str(lh_slft_Volume[subj]) + " ")
        #11
        matrix_file.write(str(lh_slfp_Volume[subj]) + " ")
        #12
        matrix_file.write(str(unc_data[subj]) + " ")
        #13
        matrix_file.write(AWC[subj] + " ")
        #14
        matrix_file.write(str(int(mom_ed[subj])<=6))
        matrix_file.write("\n")
