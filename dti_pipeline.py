#!/usr/bin/env python

#This version of this script was created on 8/24/13

# Convert dicom 2 nrrd
def dicom2nrrd(dicomdir, out_prefix):
    import os
    from nipype.interfaces.base import CommandLine
    cmd = CommandLine('DWIConvert --inputDicomDirectory %s --outputVolume %s.nrrd' % (dicomdir, out_prefix))
    cmd.run()
    return os.path.abspath('%s.nrrd' % out_prefix)

#Convert dicom 2 nii
def dicom2nii(dicomdir, subject):
    import os
    from nipype.interfaces.base import CommandLine
    from glob import glob
    out_dir = os.getcwd()
    os.environ["PATH"] += os.pathsep + '/software/mricron/'
    cmd = CommandLine('dcm2nii -o %s -p n %s*' % (out_dir, dicomdir))
    cmd.run()
    nii = os.path.abspath(glob('*nii.gz')[0])
    bval = os.path.abspath(glob('*bval')[0])
    bvec = os.path.abspath(glob('*bvec')[0])
    return nii, bval, bvec

# run through DTIPrep
def dtiprep(in_file):
    from glob import glob
    import os
    from nipype.interfaces.base import CommandLine
    os.environ["ITK_GLOBAL_DEFAULT_NUMBER_OF_THREADS"] = "1"
    cmd = CommandLine('DTIPrep -w %s -c -d -p default.xml' % in_file)
    cmd.run()
    
    qcfile = os.path.abspath(glob('*QC*nrrd')[0])
    xmlfile = os.path.abspath(glob('*QC*xml')[0])
    sumfile = os.path.abspath(glob('*QC*txt')[0])
    
    return qcfile, xmlfile, sumfile


def get_excluded_vols(in_file): # in_file is the xmlqcresult file that dtiprep outputs
    f = open(in_file, 'r')
    prev_line = ''
    bad_vols = []
    for line in f:
	if 'EXCLUDE_SLICECHECK' in line and 'gradient' in prev_line:
	    bad_vols.append(int(prev_line.split('_')[1][0:4]))
	prev_line = line
    f.close()
    return bad_vols  #array of integers that are volume #'s rejected by dtiprep

#reformat the bval and bvec files to the form that tracula expects
def transpose(bval, bvec, subject):
    import numpy as np
    import os
    bval_file = np.loadtxt(bval)
    bval_file = bval_file.transpose()
    np.savetxt('%s.bval'%(subject), bval_file, fmt='%1.0f')
    bvec_file = np.loadtxt(bvec)
    bvec_file = bvec_file.transpose()
    np.savetxt('%s.bvec'%(subject), bvec_file, fmt = '%1.14f')
    bval_return = os.path.abspath('%s.bval'%(subject))
    bvec_return = os.path.abspath('%s.bvec'%(subject))
    return bval_return, bvec_return

#Remove bad volumes from the bval and bvec files
def clean_b_files(to_remove, bval, bvec, subject):
    import os
    bval = open(bval, 'r')
    bvec = open(bvec, 'r')
    qc_bval = open('%s_QCed.bval'%(subject), 'w')
    qc_bvec = open('%s_QCed.bvec'%(subject), 'w')
    counter = 0
    for line in bval:
	if counter not in to_remove:
	    qc_bval.write(line)
    	counter += 1
    counter = 0
    for line in bvec:
	if counter not in to_remove:
	    qc_bvec.write(line)
    	counter += 1
    bval.close()
    bvec.close()
    qc_bval.close()
    qc_bvec.close()
    bval_return = os.path.abspath('%s_QCed.bval'%(subject))
    bvec_return = os.path.abspath('%s_QCed.bvec'%(subject))
    return bval_return, bvec_return

#Remove bad volumes from the nifti file
def remove_vols(in_file, to_remove, subject):
    import os
    from nipype.interfaces.base import CommandLine
    cmd = CommandLine('mkdir temp')
    cmd.run()
    cmd = CommandLine('fslsplit %s temp/%s_split' % (in_file, subject))
    cmd.run()
    print "Removing volumes", to_remove, "..."
    for vol in to_remove:
        vol = str(vol)
	cmd = CommandLine('rm -f temp/*split*%s*' % (vol))
	cmd.run()
    cmd = CommandLine('fslmerge -t %s_QCed.nii.gz temp/%s_split*' % (subject, subject)) #Do we want to include a manual exclusion option here?
    cmd.run()
    cmd = CommandLine('rm -rf temp')
    cmd.run()
    return os.path.abspath('%s_QCed.nii.gz'%(subject))  

#Get the number of b zero volumes to enter into the tracula configuration file
def get_num_bzeros(bval_path):
    bval = open(bval_path, 'r')
    num_bzeros = 0
    line = bval.readline()
    while line.strip() == '0':
	    num_bzeros += 1
            line = bval.readline()
    print "Number of b zero volumes: ", num_bzeros
    bval.close()
    return num_bzeros

#Generate configuration file for tracula
def make_config(nifti, subject, bval, bvec):
    import os
    from glob import glob
    import sys
    out_dir = os.getcwd()
    subj_dir = os.environ.get('SUBJECTS_DIR')
    split = os.path.split(nifti)
    nifti_path = split[0]
    nifti_file = split[1]
    num_bzeros = get_num_bzeros(bval)
    config = open('tracula_config.sh', 'w')
    config.write('#!bin/sh\n') 
    config.write('setenv SUBJECTS_DIR %s\n'%(subj_dir))
    config.write('set dtroot=%s\n'%(out_dir))
    config.write('set subjlist=( %s )\n'%(subject))
    config.write('set dcmroot=%s\n'%(nifti_path))
    config.write('set dcmlist=( %s )\n'%(nifti_file))
    config.write('set runlist=(1)\n')
    config.write('set bvecfile=%s\n'%(bvec))
    config.write('set bvalfile=%s\n'%(bval))
    config.write('set nb0 = %s\n'%(num_bzeros)) 
    config.write('set doeddy = 1\n')
    config.write('set dorotbvecs = 1\n')
    config.write('set thrbet = 0.5\n') #can alter this if masking seems off
    config.write('set doregflt = 0\n')
    config.write('set doregbbr = 1\n')
    config.write('set doregmni = 1 \n')
    config.write('set mnitemp = $FSLDIR/data/standard/MNI152_T1_1mm_brain.nii.gz\n')
    config.write('set doregcvs = 0 \n')
    config.write('set cvstemp = cvs_avg35\n')
    config.write('set cvstempdir = $FREESURFER_HOME/subjects\n')
    config.write('set pathlist = ( lh.cst_AS rh.cst_AS lh.ilf_AS rh.ilf_AS lh.unc_AS rh.unc_AS fmajor_PP fminor_PP lh.atr_PP rh.atr_PP lh.cab_PP rh.cab_PP lh.ccg_PP rh.ccg_PP lh.slfp_PP rh.slfp_PP lh.slft_PP rh.slft_PP)\n')
    config.write('set ncpts = (6 6 5 5 5 5 7 5 5 5 5 5 4 4 5 5 5 5)\n')
    config.write('set trainfile = $FREESURFER_HOME/trctrain/trainlist.txt\n')
    config.write('set nstick = 2\n')
    config.write('set nburnin = 200\n')
    config.write('set nsample = 7500\n')
    config.write('set nkeep = 5\n')
    config.write('set reinit = 0\n')

#Run tracula preprocessing
def trac_prep(subject):
    import os
    import sys
    from nipype.interfaces.base import CommandLine
    from glob import glob
    current_dir = os.getcwd()
    if os.path.isfile('%s/tracula_config.sh'%(current_dir)):
    	cmd = CommandLine('trac-all -prep -c %s/tracula_config.sh'%(current_dir))
    	cmd.run()
    else:
    	sys.exit("Cannot find configuration file needed for tracula")
    bvalfile = '%s/%s/dmri/bvals'%(current_dir, subject)
    bvecfile = '%s/%s/dmri/bvecs'%(current_dir, subject)
    dwi = '%s/%s/dmri/dwi.nii.gz'%(current_dir, subject)
    mask = '%s/%s/dlabel/diff/aparc+aseg_mask.bbr.nii.gz'%(current_dir, subject) #Will tracula always use this file?
    return bvalfile, bvecfile, dwi, mask

#Run bedpostx and move around some files to agree with what trac-all -path expects
def bedpostx(dwi, bval, bvec, mask, subject):
    import os
    from nipype.interfaces.base import CommandLine
    current = os.getcwd()
    cmd = CommandLine('python /mindhive/gablab/satra/code/dmri/bedpostx.py --dwi %s --bvecs %s --bvals %s --mask %s --subject %s -o %s'%(dwi, bvec, bval, mask, subject, current))
    cmd.run()
    cmd = CommandLine('mkdir %s/%s/dmri.bedpostX'%(current, subject))
    cmd.run()
    cmd = CommandLine('mv %s/%s/mean* %s/%s/dmri.bedpostX'%(current, subject, current, subject))
    cmd.run()
    cmd = CommandLine('mv %s/%s/merged* %s/%s/dmri.bedpostX'%(current, subject, current, subject))
    cmd.run()
    cmd = CommandLine('mv %s/%s/dyad* %s/%s/dmri.bedpostX'%(current, subject, current, subject))
    cmd.run()
    cmd = CommandLine('cp %s/trac_bedp/trac_bedp_postproc_merge_mean_dsamples/mean_dsamples_merged.nii.gz %s/%s/dmri.bedpostX/mean_dsamples.nii.gz'%(current, current, subject))
    cmd.run()

#Run trac-all -path
def trac_path():
    import os
    from nipype.interfaces.base import CommandLine
    current_dir = os.getcwd()
    cmd = CommandLine('trac-all -path -c %s/tracula_config.sh'%(current_dir))
    cmd.run()

#Make tables of the FA values from the tracula output
def make_tables(subject):   #Could make one for each output stat
    import os
    from nipype.interfaces.base import CommandLine
    current = os.getcwd()
    tract_path = '%s/%s/dpath'%(current, subject)
    for tract in os.listdir(tract_path):
	if 'merged' not in tract:
	   cmd = CommandLine('tractstats2table --inputs %s/%s/pathstats.byvoxel.txt --byvoxel --byvoxel-measure FA --tablefile %s/%s/pathstats.byvoxel.FA.table'%(tract_path,tract,tract_path,tract))
           cmd.run()

from argparse import ArgumentParser
if __name__ == "__main__":
     parser = ArgumentParser()
     parser.add_argument("--dicomdir", dest="dicomdir", help="dicomdir", required=True)
     parser.add_argument("--subject", dest="subject", help="subject id", required=True)
     args = parser.parse_args()


# run everything

     nrrd_file = dicom2nrrd(args.dicomdir, args.subject) 
     qcfile, xmlfile, _ = dtiprep(nrrd_file)
     nifti, bval, bvec = dicom2nii(args.dicomdir, args.subject)
     bad_vols = get_excluded_vols(xmlfile)
     bval, bvec = transpose(bval, bvec, args.subject) 
     if len(bad_vols) > 0:
        bval, bvec = clean_b_files(bad_vols, bval, bvec, args.subject)
        nifti = remove_vols(nifti, bad_vols, args.subject)       
     else:
          print "No bad volumes detected"
     make_config(nifti, args.subject, bval, bvec)
     bval, bvec, dwi, mask = trac_prep(args.subject)
     bedpostx(dwi, bval, bvec, mask, args.subject)
     trac_path()
     make_tables(args.subject)

