from fit_gain import full_routine, initialize_paths
#TODO: 
# review additional dates (aug) and make notes
# compare results in data log and see if any details will help. figure out how to incorporate log data into analysis
# figure out pulser offset question
#figure out purpose of calibration datasets and "pulser runs" 
# put titles and maybe folders on title of plot
# get output of fits to save to cumulative data file for input into bigger fit routine
# ask for automated data example from other projects

date = "5-7-2025"
#notes: try to find out what calibration plot is showing
# only 1 successful fit to pulser peak @ 3600D_2900G_90-10_CG10_FG0p5
# all others show two other peaks at other locations -> mismatch betwen settings? check log

###################
date = "5-9-2025"
#notes: calibration sweep is roughly the same as above
#  "" 3600D_2900G_90-10_CG10_FG0p5

##################
date = "5-11-2025"
#notes: one file, no successful fit, w extra peaks @ bad locs

##################
date = "5-13-2025"
#notes: no fit to pulser

##################
date = "5-17-2025"
#notes: not parsed, no fits to pulser

##################
date = "5-19-2025"
#notes: labled _pad, may indidcate that prior data was taken w strip, which would offset pulser
# one fit to pulser: D3600_G3150_CG10_FG0p5_pad
##################
date = "5-28-2025"
#notes: 5 good pulser fits! 
# a very asymmetric gaussian @ 3900D_3300G_92-8_ArCH4_CG5_FG0p5_pad
##################
#date = "8-2-2025"
#notes: error in title, says 92-10 arco2, obviously not correct
#
##################
date = "8-11-2025"
#notes:

#input = "3600D_3050G_90-10_CG10_FG0p5.Spe"#Use file name
cwd, data_dir, spe_files = initialize_paths(date)
#input = spe_files[3]# use file from list
input = None #run thru full folder

xmax=8200 #For right bound of plot only, doesn't edit data
fitmin=0
fitmax=8200 
muinit=720
sigmainit=100

#full_routine(input, date, None,None,None,None,None)
full_routine(input, date, xmax,fitmin,fitmax,muinit,sigmainit)