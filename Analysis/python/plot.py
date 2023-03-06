# plot.py
import matplotlib.pyplot as plt

def plot(x, y, y_errs, output_file, title, x_label, y_label, x_lim, y_lim):
    plt.errorbar(x, y, yerr=y_errs, fmt='o', alpha=0.5)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xlim(x_lim)
    plt.ylim(y_lim)
    # save plot to output file
    plt.savefig(output_file)
    # close all windows to avoid combining plots
    plt.close('all')

