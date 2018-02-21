import os
import sys
import json
import pickle
from numpy import median
import math

behavioral_data = "./behavioral_data.json"
lena_data = "./lena_data.json"
time_two = "./time_two.json"
tbss_directory = "/om/user/jsegaran/tbss"
vars_file = "./vars_file.txt"
subjects_file = "subjects.txt"
motion_file = "motion.txt"
updated_file = "updated.json"
data_dir = "/om/user/jsegaran/scripts/data"

if __name__ == "__main__":


    # Taking the arguments input
    for i in range(len(sys.argv)):
        arg = sys.argv[i]

        if arg == "--tbss-directory":
            tbss_directory = sys.argv[i+1]
            i+=2
        elif arg == "--vars-file":
            var_file = sys.argv[i+1]
            i+= 2
        elif arg == "--behavioral-data":
            behavioral_data = sys.argv[i+1]
            i+=2

    # Read the files that contain the behavioral, and lena data. As well as
    # subject information

    cwd = os.getcwd()
    # Get current directory so we can go back later. Lets use relative directory # placement for tbss_dir instead of absolute

    os.chdir(data_dir)

    file = open(behavioral_data, 'r')
    behav_data = json.load(file)
    file.close()

    file = open(updated_file, 'r')
    updated_data = json.load(file)
    file.close()

    file = open(lena_data, 'r')
    lena_data = json.load(file)
    file.close()

    file = open(time_two, 'r')
    time_two = json.load(file)
    file.close()

    os.chdir(cwd)

    os.chdir(tbss_directory)

    print(tbss_directory)
    print(subjects_file)
    file = open(subjects_file, 'r')
    subjects = json.load(file)
    file.close()

    file = open(motion_file, 'r')
    total_motion_index = json.load(file)
    file.close()

    # Move to the directory where the work will be done
    os.chdir("./stats")

    matrix_file = open("design.mat", 'w')
    contrast_file = open("design.con", 'w')



    # Create the vairables that could be output. Change numVariables as
    # approproriate
    numVariables = 5
    age = behav_data['age']
    gender = behav_data['sex']
    verbal_score = behav_data['MeanVerbal_PPVT-CELF_T1']
    parent_ed = updated_data['Parent_ed_abr']
    bilingual = behav_data['mono_bi_lingual']
    ppvt_t1 = behav_data['PPVT_std_T1']
    comb_SES = behav_data['SES_avg_parentEdIncome_z']
    breif_exec = behav_data['BRIEF_Global_Executive']
    high_SES = behav_data['mom_college']
    income = updated_data['Income']
    other_motion = updated_data['TraculaMotionIndex']
    AWC = lena_data['AWC']
    CTC = updated_data['CTC']
    CVC = lena_data['CVC']
    intervention = time_two['Intervention_Assigned']
    ppvt_delta = time_two['PPVTssChange']
    mom_ed = behav_data['mom_ed']

    # Matrix Header
    matrix_file.write("/NumWaves " + str(numVariables) + "\n")
    matrix_file.write("/NumPoints " + str(len(subjects)) + "\n")
    matrix_file.write("/Matrix\n")

    # This demeans the variable

    for subj in sorted(verbal_score.keys()):

        # Modify this to select the variables of use
        if subj not in subjects:
            continue

        matrix_file.write("1 ")

        # if intervention[subj] == "0":
        #     matrix_file.write("1 0 " + ppvt_delta[subj] + " ")
        # else:
        #     matrix_file.write("0 1 " + ppvt_delta[subj] + " ")

        # matrix_file.write(ppvt_delta[subj] + " ")
        # matrix_file.write(intervention[subj] + " ")
        # if high_SES[subj] <= "0":
        #     matrix_file.write("1 0 " + CTC[subj] + " 0 ")
        # else:
        #     matrix_file.write("0 1 0 " + CTC[subj] + " ")
        # matrix_file.write(CTC[subj] + " ")
        # matrix_file.write(ppvt_t1[subj] + " ")
        #matrix_file.write(str(mom_ed[subj]) + "  ")
        # matrix_file.write(comb_SES[subj] + " ")
        # matrix_file.write(bilingual[subj] + " ")
        # matrix_file.write(intervention[subj] + " ")
        # matrix_file.write(str(math.log(int(income[subj]))) + " ")
        matrix_file.write(verbal_score[subj] + " ")
        matrix_file.write(parent_ed[subj] + " ")
        matrix_file.write(income[subj] + " ")
        matrix_file.write(age[subj] + " ")
        matrix_file.write(gender[subj] + " ")
        matrix_file.write(str(total_motion_index[subj]) + " ")
        # matrix_file.write(other_motion[subj] + " ")
        matrix_file.write("\n")

    #Outputing the contrast file
    contrast_file.write("/NumWaves " + str(numVariables) + "\n")
    contrast_file.write("/NumContrasts " + str(1) + "\n")
    contrast_file.write("/Matrix\n")
    # Generates basic  contras
    # contrast_file.write("0.000000e+00 1.0000e+0")
    # contrast_file.write("0.000000e+00 1.0000e+0 00.000000e+00 \n")
    # contrast_file.write("0.000000e+00 -1.0000e+0 00.000000e+00 \n ")
    # contrast_file.write("0.0000e+00 0.000000e+00 1.0000e+00 -1.000000e+00\n")
    # contrast_file.write("0.0000e+00 0.000000e+00 -1.0000e+00 1.000000e+00\n")
    # contrast_file.write("0.0000e+00 0.000000e+00 -1.0000e+00 -1.000000e+00\n")
    # contrast_file.write("0.0000e+00 0.000000e+00 1.0000e+00 1.000000e+00\n")
    # contrast_file.write("0.0000e+00 0.000000e+00 -1.0000e+00 0.0000e+00\n")
    # contrast_file.write("0.0000e+00 0.000000e+00 0.0000e+00 -1.000000e+00\n")
    # contrast_file.write("0.0000e+00 0.000000e+00 1.0000e+00 0.0000e+00\n")

    contrast_file.write("0.000000e+00 1.0000e+00 0.000000e+00 0.000000e+00 0.000000e+00 0.000000e+00 0.000000e+00\n")
    # contrast_file.write("0.0000e+00 0.000000e+00 1.0000e+00 -1.000000e+00 0.0000e+00 0.0000e+00 0.0000e+00\n")
    # contrast_file.write("0.0000e+00 0.000000e+00 -1.0000e+00 1.000000e+00 0.0000e+00 0.0000e+00 0.0000e+00 \n")
    # contrast_file.write("0.0000e+00 1.0000e+00 0.0000e+00 0.0000e+00 0.0000e+00 0.0000e+00\n")
    # contrast_file.write("0.0000e+00 0.000000e+00 0.0000e+00 1.000000e+00 0.0000e+00 0.0000e+00\n")
    # contrast_file.write("0.000000e+00 1.0000e+00 0.000000e+00 0.000000e+00 0.000000e+00 0.000000e+00")

    contrast_file.close()
    matrix_file.close()
