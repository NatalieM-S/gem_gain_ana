from fit_gain import full_routine
import os
#iterate thru all folders
base = './gain_data'
folders=[]
for root, dirs, files in os.walk(base):
    folders.append(root)

for f in folders:
    f=f[len(base)+1:]
    #full_routine(None, f, 8200, 0, 8200, 720, 100)

print('====DONE=====')