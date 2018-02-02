import os
import glob

dti_dir = '/mindhive/xnat/dicom_storage/FACT/DTI_dcm/'
#subject_list = '/mindhive/gablab/u/jlnrd/DTI_preproc/subject_list_dti.txt'
subject_list = sorted(glob.glob('/mindhive/xnat/dicom_storage/FACT/DTI_dcm/FACT_???'))

num_grad=[]

for sub in subject_list:
    subid = sub.split('/')[-1]
    with open(os.path.join(dti_dir, subid, '%s_QCReport.txt' %subid), 'r') as f:
        count =0        
        for line in f:
            if len(line.split()) == 5:
                line1, line2 = line.split()[0], line.split()[1]
                if line1 == 'Included' and line2 == 'Gradients:':
                    num_gradients = line.split()[4]
            if len(line.split()) == 4:
                 line1 = line.split()[0]
                 if line1 == 'Baselines_indices:':
                    count = count +1
                    num_b0=count
        num_grad.append('%s\t%s\t%s\n' % (subid, num_gradients,num_b0))

with open('/mindhive/gablab/u/jlnrd/DTI_preproc/DTI_num_gradients.txt', 'w') as wf:
    wf.writelines(num_grad)






