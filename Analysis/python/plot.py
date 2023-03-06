# plot.py
import matplotlib.pyplot as plt

def plot(x, y, y_errs, output_file, title, x_label, y_label):
    plt.errorbar(x, y, yerr=y_errs, fmt='o')
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    # save plot to output file
    plt.savefig(output_file)
    # close all windows to avoid combining plots
    plt.close('all')

