from fit_gain import full_routine, initialize_paths
date = "5-11"
date = date +"-2025"
mode = 1

# mode options: 
#0: None as inputs (manual fits)
#1: Use guesses enumerated below for (manual) fit
#2: Editable input for testing
#
#10,11,12: 0,1,2 with input for specific file

#todo: still doesnt autoeval all subfolders, need to be added to date string manually

#date = "5-7-2025"
#notes: try to find out what calibration plot is showing
# only 1 successful fit to pulser peak @ 3600D_2900G_90-10_CG10_FG0p5
# all others show two other peaks at other locations -> mismatch betwen settings? check log

###################
#date = "5-9-2025"
#notes: calibration sweep is roughly the same as above
#  "" 3600D_2900G_90-10_CG10_FG0p5

##################
#date = "5-11-2025"
#notes: one file, no successful fit, w extra peaks @ bad locs

##################
#date = "5-13-2025"
#notes: no fit to pulser

##################
#date = "5-17-2025"
#notes: not parsed, no fits to pulser

##################
#date = "5-19-2025"
#notes: labled _pad, may indidcate that prior data was taken w strip, which would offset pulser
# one fit to pulser: D3600_G3150_CG10_FG0p5_pad
##################
#date = "5-28-2025"
#notes: 5 good pulser fits! 
# a very asymmetric gaussian @ 3900D_3300G_92-8_ArCH4_CG5_FG0p5_pad

##################
#date = "8-2-2025"
#notes: error in title, says 92-10 arco2, obviously not correct
#

##################
#date = "8-11-2025"
#notes:
#
#

##################
#date = "8-13-2025"
#notes:
#
#

##################
#basedate = "8-15-2025"
#date=basedate+'/18p5psi'
#date=basedate+'/29p5psi'
#date=basedate+'/44psi'
#notes:
#
#

##################
#basedate = "8-18-2025"
#date=basedate+'/36psi'
#date=basedate+'/44psi'
#date=basedate+'/50p5psi'
#notes:
#
#

##################
#basedate = "8-19-2025"
#date=basedate+'/14p5psi'
#date=basedate+'/18p5psi'
#date=basedate+'/22psi'
#date=basedate+'/29p5psi'
#notes:
#
#

##################
#basedate = "8-20-2025"
#date=basedate+'/22.0'
#date=basedate+'/29.5'
#date=basedate+'/36.0'
#date=basedate+'/44.0'
#date=basedate+'/50.5'
#notes:
#
#

##################
#basedate = "8-21-2025"
#date=basedate+'/pulser_runs/116mVpp'
#date=basedate+'/pulser_runs/166mVpp'
#date=basedate+'/pulser_runs/222mVpp'
#notes: calibrations are stored in output

##################
#basedate = "8-20-2025"
#date=basedate+"/22.0"
#notes:

##################
#basedate = "8-22-2025"
#date=basedate+'/29.5'
#date=basedate+'/29.5_Nat_Tutorial'
#date=basedate+'/36.0'
#date=basedate+'/44.0'
#date=basedate+'/50.5'
#notes:
#
#

##################
#basedate = "8-25-2025"
#date=basedate+'/22.0'
#date=basedate+'/29.5'
#date=basedate+'/36.0'
#date=basedate+'/44.0'
#date=basedate+'/50.5'
#date=basedate+'/54.5'
#date=basedate+'/59.0'
#notes:
#
#

##################
#basedate = "8-26-2025"
#date=basedate+'/15'
#date=basedate+'/AmbientOriginalPosition'
#date=basedate+'/AmbientUpdatedPosition'
#notes:
#
#


#input_file = "3600D_3050G_90-10_CG10_FG0p5.Spe"#Use file name
cwd, data_dir, spe_files = initialize_paths(date)
for n in range(len(spe_files)):
    print(n,spe_files[n])
input_file = None #run thru full folder
if mode >9:
    n=input("Input file number to run: ")
    input_file = spe_files[int(n)]# use file from list
    mode = mode-10


xmax=8200 #For right bound of plot only, doesn't edit data
fitmin=0
fitmax=8200 
muinit=720
sigmainit=100

match mode:
    case 0:
        full_routine(input_file, date, None,None,None,None,None)
    case 1:
        full_routine(input_file, date, xmax,fitmin,fitmax,muinit,sigmainit)
    case 2: 
        full_routine(input_file, date, 1000,None,1000,None,None,skip_confirm=True)
