# gem_gain_ana
Analysis for GEM gain measurements
## Setup
### Windows Setup
cd gem_gain_ana  
~~python setup.py~~ not needed anymore
### Linux Setup
cd gem_gain_ana  
source setup.sh

todo: test w/+ w/out setup.sh on linux

## run
python fit_gain.py -d 5-7-2025 -i D3600_G3000_~_90-10_CG10_FG0p5_psi~.Spe --xmax 1200 --fitmin 650 --fitmax 1000

Plots are saved to `/output/<date>/s`

## layout
```
gain_data/          # Input data
output/             # Saved outputs 
fit_gain.py         # analysis script
draw_HV_vs_gain_overlay.py  # Plotting 
```

## Usage

### Basic 

```
python fit_gain.py -d <date> -i <filename>.Spe 
```

### Options
```
Required:
  -d, --date FOLDER       Date folder under gain_data/ (fmt: 5-7-2025)
 

Analysis:
  -i, --input FILE        data filename(s) (ex: D3600_G3000_~_90-10_CG10_FG0p5_psi~.Spe), leave blank to analyze full folder

  --xmax INT              X-axis upper limit (default: 8200)
  --fitmin INT            Min channel for peak fit (default: 0)
  --fitmax INT            Max channel for peak fit (default: 8200)
  --muinit FLOAT          Initial Gaussian mean guess (default: 720)
  --sigmainit FLOAT       Initial Gaussian sigma guess (default: 100)
  --auto                  Auto generate fit parameters. If not used: Select fit parameters interactively on graph
  --pulser-min FLOAT      (optional) lower bound for pulser search
  --pulser-max FLOAT      (optional) upper bound for pulser search
```

### Examples

Single file
```
python fit_gain.py -d 5-7-2025 -i D3600_G3000_~_90-10_CG10_FG0p5_psi~.Spe
```

With fit range
```
python fit_gain.py -d 5-7-2025 -i D3600_G3050_~_90-10_CG10_FG0p5_psi~.Spe --xmax 1500 --fitmin 900 --fitmax 1400 --muinit 1100 --sigmainit 80
```

Batch process all files in a date folder:
```
python fit_gain.py -d 5-7-2025 
todo: make this work for subfolders in date folders too
```
Can input >=1 filenames after `-i`. Use `--auto` to generate fits automatically (Work in progress), otherwise click the plot to generate input parameters. Fit vals and log details are saved to `output/fit_results.csv`. 

## Data Format
Input data files are .Spe   
Filenames encode expt parameters  
Filenames were irregular and have been regularized using regularize_filenames.py   
May not be complete, but sufficient for existing dataset  

```
D<V Drift>_
G<V GEM>_
Gas_<Gas mix ratio>_
CG<coarse gain>_
FG<fine gain>
psi<pressure>.Spe

Example: D3050_G2550_ArCH4_92-8_CG20_FG0p5_psi14p5.Spe
```

