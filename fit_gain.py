import os
import matplotlib.pyplot as plt
import argparse
import numpy as np
from scipy.optimize import curve_fit
from pathlib import Path

GAIN_DATA_DIR = None  #default: cwd + "\gain_data"
GEM_WORKING_DIR = None  # default: cwd

def parse_filename_info(filename):
    name = os.path.splitext(os.path.basename(filename))[0]
    try:
        drift_str = name.split('_')[0].replace('D', '')
        gem_str = name.split('_')[1].replace('G', '')
        ratio = name.split('_')[2]
        cg = name.split('_')[3].replace('CG', '')
        fg = name.split('_')[4].replace('FG', '').replace('p', '.')

        label = (
            f"Drift: {drift_str} V\n"
            f"GEM: {gem_str} V\n"
            f"Ar:CO₂ = {ratio}\n"
            f"Coarse Gain: {cg}\n"
            f"Fine Gain: {fg}"
        )
        return label
    except Exception:
        return "Parameter info not parsed"

def gaussian(x, a, mu, sigma):
    return a * np.exp(- (x - mu)**2 / (2 * sigma**2))

def gauss_plus_pol2(x, a, mu, sigma, c0, c1, c2):
    gauss = a * np.exp(- (x - mu)**2 / (2 * sigma**2))
    poly = c0 + c1 * x + c2 * x**2
    return gauss + poly

def draw_spec_histogram(filepath, output_path, param_text, xmax, fitmin, fitmax, muinit=720, sigmainit=100):
    counts = []

    with open(filepath, 'r') as f:
        for line in f:
            if "$DATA:" in line:
                break

        first_bin, last_bin = map(int, f.readline().split())
        nbins = last_bin - first_bin + 1

        for line in f:
            line = line.strip()
            if not line:
                continue
            counts.append(int(line))
            if len(counts) >= nbins:
                break

    x = np.arange(first_bin, last_bin + 1)
    y = np.array(counts)

    mask = (x >= fitmin) & (x <= fitmax)
    x_fit = x[mask]
    y_fit = y[mask]
    
    # Fit Gaussian the 5.9 keV peak
    a0 = np.max(y)
    mu0 = muinit
    sigma0 = sigmainit
    try:
        popt, pcov = curve_fit(gaussian, x_fit, y_fit, p0=[a0, mu0, sigma0])
        fit_y = gaussian(x, *popt)
    except RuntimeError:
        popt = [0, 0, 0]
        fit_y = np.zeros_like(x)

        
    # Plot
    plt.figure(figsize=(10, 5))
    plt.plot(x, y, drawstyle='steps-mid', label='Data')
    plt.plot(x, fit_y, 'r--', label=f'5.9 keV Fit\n$\\mu$={popt[1]:.1f}, $\\sigma$={popt[2]:.1f}')
    plt.axvspan(fitmin, fitmax, color='Red', alpha=0.1, label='Fit range')

    ## CG 10 FG 0.5 of strip
    #pulser_x_min = 112
    #pulser_x_max = 120

    ## CG 10 FG 0.5 of pad
    pulser_x_min = 225
    pulser_x_max = 245

    ## CG 50 FG 0.5 strip
    #pulser_x_min = 600
    #pulser_x_max = 650

    mask_fixed = (x >= pulser_x_min) & (x < pulser_x_max)

    x_fixed = x[mask_fixed]
    y_fixed = y[mask_fixed]

    ratio_mu = 0.

    if len(x_fixed) > 3:
        a1 = np.max(y_fixed)
        mu1 = x_fixed[np.argmax(y_fixed)]
        sigma1 = 1.0

    try:
        popt2, _ = curve_fit(gaussian, x_fixed, y_fixed, p0=[a1, mu1, sigma1])
        fit_y2 = gaussian(x, *popt2)

        fivep9_fit_mu = popt[1] if len(popt) > 1 else None
        pulse_fit_mu = popt2[1] if 'popt2' in locals() and len(popt2) > 1 else None

        ratio_mu =  fivep9_fit_mu / pulse_fit_mu if fivep9_fit_mu and pulse_fit_mu else None
        label2 = f"Pulse Peak\n$\\mu$={popt2[1]:.2f}, $\\sigma$={popt2[2]:.2f}"

        plt.plot(x, fit_y2, 'g--', label=label2)

    except RuntimeError:
        pass

    plt.xlim(0., xmax)
    plt.xlabel("Channels [ADC]")
    plt.ylabel("Counts")
    plt.title("");

    if ratio_mu:
        param_text = param_text + f"\n$\\mu_{{\\mathrm{{5.9 keV}}}}/\\mu_{{\\mathrm{{Pulse}}}}$={ratio_mu:.3f}"

        
    #plt.text(0.97, 0.95, param_text, transform=plt.gca().transAxes,
    #         verticalalignment='top', horizontalalignment='right',
    #         fontsize=10, bbox=dict(boxstyle="round,pad=0.3", facecolor='white', alpha=0.5))
    plt.axvspan(pulser_x_min, pulser_x_max, color='green', alpha=0.1, label='Fit Range')
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    # Save plot
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    print(f"Plot saved to {output_path}")
    plt.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Draw histogram from .Spe file")
    #parser.add_argument("-i", "--input", required=True, help="Name of the .Spe file (e.g., myfile.Spe)")
    parser.add_argument("-d", "--date", required=True, help="Subdirectory name under gain_data/")
    parser.add_argument("-i", "--input", default=None, help="Name of the .Spe file (e.g., myfile.Spe)")
    parser.add_argument("--xmax", type=int, default=8200, help="Set upper limit for x-axis")
    parser.add_argument("--fitmin", type=int, default=0, help="Minimum x value for fit")
    parser.add_argument("--fitmax", type=int, default=8200, help="Maximum x value for fit")
    parser.add_argument("--muinit", type=float, default=720, help="Initial guess for Gaussian mean (mu)")
    parser.add_argument("--sigmainit", type=float, default=100, help="Initial guess for Gaussian sigma")
    args = parser.parse_args()

    # Use input, env var or default paths
    data_dir = GAIN_DATA_DIR or os.environ.get("GAIN_DATA_DIR")
    cwd = GEM_WORKING_DIR or os.environ.get("GEM_WORKING_DIR")
    
    # use default if not set
    if not cwd:
        #cwd = Path.cwd()
        cwd = Path(__file__).resolve().parent
    if not data_dir:
        data_dir = cwd/"gain_data"
    if data_dir.is_dir():
        subdir = data_dir / args.date
        #spe_files = list(data_dir.glob("**/*.Spe"))
        spe_files = list(subdir.glob("*.Spe"))
        print(f"{len(spe_files)} .Spe files found in /{args.date}/")
    else:
        raise FileNotFoundError('gain data directory not found at cwd/gain_data')

    if args.input:
        spe_files=[args.input]
    for input in spe_files:
        # Full input file path
        input_path = os.path.join(data_dir, args.date, input)

        # Output plot path
        input_name_wo_ext = os.path.splitext(input)[0]
        rel_path = os.path.relpath(input_path,data_dir)[0:-4]
        #output_path = os.path.join(cwd, "output", args.date, f"{input_name_wo_ext}.pdf")
        output_path = os.path.join(cwd, "output", f"{rel_path}.pdf")
        # run info
        param_text = parse_filename_info(input)
        
        draw_spec_histogram(input_path, output_path, param_text, xmax=args.xmax, fitmin=args.fitmin, fitmax=args.fitmax, muinit=args.muinit, sigmainit=args.sigmainit)
