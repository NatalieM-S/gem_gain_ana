import matplotlib.pyplot as plt

def draw_spec_histogram(filename=""):
    counts = []

    with open(filename, 'r') as f:
        # Skip lines until "$DATA:" is found
        for line in f:
            if "$DATA:" in line:
                break

        # Read "0 8191"
        first_bin, last_bin = map(int, f.readline().split())
        nbins = last_bin - first_bin + 1  # Should be 8192

        # Read 8192 values
        for line in f:
            line = line.strip()
            if not line:
                continue
            counts.append(int(line))
            if len(counts) >= nbins:
                break

    # Plot the histogram
    plt.figure(figsize=(10, 5))
    plt.plot(range(first_bin, last_bin + 1), counts, drawstyle='steps-mid')
    plt.xlabel("Channel")
    plt.ylabel("Counts")
    plt.title("Spectrum Histogram")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

draw_spec_histogram("3600D_3000G_90-10_CG10_FG0p5.Spe")
