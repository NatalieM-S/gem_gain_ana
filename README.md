# gem_gain_ana
Analysis for GEM gain measurements
## Setup
### Windows Setup
cd gem_gain_ana  
~~python setup.py~~ not needed anymore
### Linux Setup
cd gem_gain_ana  
setup.sh

todo: test without setup.sh on linux

## run
python fit_gain.py -d 5-7-2025 -i 3600D_3000G_90-10_CG10_FG0p5.Spe --xmax 1200 --fitmin 650 --fitmax 1000

Plots are saved to `/output/<date>/<filename>.pdf`

## layout
```
gain_data/          # Input data
results/            # Saved outputs 
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
  -i, --input FILE        data filename (ex: 3600D_3000G_90-10_CG10_FG0p5.Spe), leave blank to analyze full folder

  --xmax INT              X-axis upper limit (default: 8200)
  --fitmin INT            Min channel for peak fit (default: 0)
  --fitmax INT            Max channel for peak fit (default: 8200)
  --muinit FLOAT          Initial Gaussian mean guess (default: 720)
  --sigmainit FLOAT       Initial Gaussian sigma guess (default: 100)
```

### Examples

Single file
```
python fit_gain.py -d 5-7-2025 -i 3600D_3000G_90-10_CG10_FG0p5.Spe
```

With fit range
```
python fit_gain.py -d 5-7-2025 -i 3600D_3050G_90-10_CG10_FG0p5.Spe --xmax 1500 --fitmin 900 --fitmax 1400 --muinit 1100 --sigmainit 80
```

Batch process all files in a date folder:
```
python fit_gain.py -d 5-7-2025 

```
todo: either allow for vector inputs or manual guesses you can input by clicking on graph or by inputting while viewing graph or better fitting algorithm... 

## Data Format
Input data files are .Spe   
Filenames encode expt parameters
```
<V Drift>D_
<V GEM>G_
<Gas mix ratio>_
CG<coarse gain>_
FG<fine gain>.Spe

Example: 3600D_3000G_90-10_CG10_FG0p5.Spe
```