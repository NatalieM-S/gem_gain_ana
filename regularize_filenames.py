import re
import os

'''
produces several types of filenames
missing values are filled with ~
--------------
Standard: 

D3050_G2550_ArCH4_92-8_CG20_FG0p5_psi14p5.Spe

--------------
Prefix/suffix:

D3650_G3150_ArCO2_90-10_CG5_FG0p5_psi18p5_amp166.Spe
gain_D3650_G3150_ArCH4_95-5_CG5_FG0p5_psi~.Spe

--------------
Truncated: 

amp166mvpp_CG200_FG0p5.Spe
calib_CG10_FG0p5.Spe

'''

def regularize_filename(filename):
    filename = filename.lower()

    if not filename.endswith('.spe'):
        return None

    name, _ = os.path.splitext(filename)
    
    #  values to extract
    data = {"prefix": "", "d": "~", "g": "~", "gas": "~", 
        "ratio": "~", "cg": "~", "fg": "~", "psi": "~", "suffix": ""}

    # 1  Prefix
    prefix_match = re.search(r'(gain_|calib_|amp\d+[^_]*_|amp_)', name)
    if prefix_match:
        data["prefix"] = prefix_match.group(0)
        name = name.replace(prefix_match.group(0), " ")

     # 2  CG
    cg_match = re.search(r'cg(\d+)', name)
    if cg_match:
        data["cg"] = cg_match.group(1)
        name = name.replace(cg_match.group(0), " ")

    # 3 FG
    fg_match = re.search(r'fg(\d+p\d+|\d+\.\d+)', name)
    if fg_match:
        data["fg"] = fg_match.group(1)#.replace('p', '.')
        name = name.replace(fg_match.group(0), " ")

    # 4 divider voltage (D)
    d_match = re.search(r'(\d+)\s*d|d\s*(\d+)', name)
    if d_match:
        data["d"] = d_match.group(1) or d_match.group(2)
        name = name.replace(d_match.group(0), " ")

    # 5 gem voltage (G)
    g_match = re.search(r'(\d+)\s*g|g\s*(\d+)', name)
    if g_match:
        data["g"] = g_match.group(1) or g_match.group(2)
        name = name.replace(g_match.group(0), " ")

    # 6 Gas
    if re.search(r'ar_?ch4', name):
        data["gas"] = "ArCH4"
        name = re.sub(r'[-_]?ar_?ch4', " ", name)
    elif re.search(r'ar_?co2|arc\)2', name):
        data["gas"] = "ArCO2"
        name = re.sub(r'[-_]?ar_?co2|arc\)2', " ", name)

    # 7 gas ratio 
    ratio_match = re.search(r'(\d{1,3})[-_](\d{1,3})', name)
    if ratio_match:
        # Still check that it's likely a ratio (<=100)
        if int(ratio_match.group(1)) <= 100:
            data["ratio"] = f"{ratio_match.group(1)}-{ratio_match.group(2)}"
            name = name.replace(ratio_match.group(0), " ")

    # 8 psi
    psi_match = re.search(r'psi(\d+p?\d*)', name)
    if psi_match:
        data["psi"] = psi_match.group(1)#.replace('p', '.')
        name = name.replace(psi_match.group(0), " ")

    # 9 suffix
    suffix_match = re.search(r'(_pad.*|_bis.*|_rerun.*|_strange.*|_amp166.*|_fe55.*)', name)
    if suffix_match:
        data["suffix"] = suffix_match.group(0)
        name = name.replace(suffix_match.group(0), " ")

    #check for errors
    if re.search(r'[^_\s]', name):
        print(filename)
        print(name)

    #make filename
    if "amp" in data["prefix"] or "calib" in data["prefix"]:
        new_name = f"{data['prefix']}CG{data['cg']}_FG{data['fg']}{data['suffix']}"
    else:
        new_name = (f"{data['prefix']}D{data['d']}_G{data['g']}_{data['gas']}_{data['ratio']}_CG{data['cg']}_FG{data['fg']}_psi{data['psi']}{data['suffix']}")

    new_name = re.sub(r'_{2,}', '_', new_name).strip('_')
    return new_name + ".Spe"

check_names = 0
rename_all = 0


print(f"{'ORIGINAL':<60} | {'REGULARIZED'}")
print("-" * 120)

filenames,filepaths = [],[]
for root, dirs, files in os.walk("./gain_data"):
    for f in files:
        if check_names:
            reg = regularize_filename(f)
            if reg:
                print(f"{f:<60} | {reg}")
            else:
                print(f"{f:<60} | [SKIPPED]")
        if rename_all:
            reg = regularize_filename(f)
            if reg:
                if not check_names:
                    print(f"{f:<60} | {reg}")
                original_path = os.path.join(root, f)
                new_path = os.path.join(root, reg) 
                os.rename(original_path,new_path)
