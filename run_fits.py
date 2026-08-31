from fit_gain import full_routine, initialize_paths
date = "5-7-2025"
cwd, data_dir, spe_files = initialize_paths(date)
xmax=8200
fitmin=0
fitmax=8200
muinit=720
sigmainit=100
full_routine(None, date, xmax,None,None,None,None)
full_routine(None, date, xmax,fitmin,fitmax,muinit,sigmainit)