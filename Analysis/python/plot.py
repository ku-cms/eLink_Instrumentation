# plot.py
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot(x, y, y_errs, output_file, title, x_label, y_label, x_lim, y_lim):
    plt.errorbar(x, y, yerr=y_errs, fmt='o', alpha=0.5)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.xlim(x_lim)
    plt.ylim(y_lim)
    # write number of points
    n_points    = len(x)
    x_diff      = x_lim[1] - x_lim[0]
    y_diff      = y_lim[1] - y_lim[0]
    text_x      = x_lim[0] + 0.10 * x_diff
    text_y      = y_lim[0] + 0.90 * y_diff
    plt.text(text_x, text_y, "Number of e-links (points): {0}".format(n_points))
    # save plot to output file
    plt.savefig(output_file)
    # close all windows to avoid combining plots
    plt.close('all')

def makeCumulativePlot(x, y, plot_dir, plot_name, title, x_label, y_label, x_lim, y_lim):
    fig, ax = plt.subplots(figsize=(10, 6))
    plt.plot(x, y, marker='o', linestyle='-', color='green', alpha=0.5)
    
    # Format x-axis to show ticks based on time interval
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SUNDAY, interval=4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    
    plt.title(title,    fontsize=20)
    plt.xlabel(x_label, fontsize=16)
    plt.ylabel(y_label, fontsize=16)
    if x_lim:
        plt.xlim(x_lim)
    if y_lim:
        plt.ylim(y_lim)
    plt.grid(True)
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()

    savePlot(plot_dir, plot_name)

    # close all windows to avoid combining plots
    plt.close('all')

def makeCumulativePlotMultiStage(cumulative_data, plot_dir, plot_name, title, x_label, y_label, x_lim, y_lim, colors):
    fig, ax = plt.subplots(figsize=(12, 6))
    for stage, cumulative_series in cumulative_data.items():
        ax.plot(cumulative_series.index, cumulative_series.values, label=stage, linestyle='-', color=colors[stage])

    # Format x-axis to show ticks based on time interval
    ax.xaxis.set_major_locator(mdates.WeekdayLocator(byweekday=mdates.SUNDAY, interval=4))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))

    plt.title(title,    fontsize=20)
    plt.xlabel(x_label, fontsize=16)
    plt.ylabel(y_label, fontsize=16)
    if x_lim:
        plt.xlim(x_lim)
    if y_lim:
        plt.ylim(y_lim)
    ax.legend()
    plt.grid(True)
    plt.xticks(rotation=45, fontsize=10)
    plt.tight_layout()

    savePlot(plot_dir, plot_name)

    # close all windows to avoid combining plots
    plt.close('all')

# save plot to png and pdf
def savePlot(plot_dir, plot_name):
    output_png = "{0}/{1}.png".format(plot_dir, plot_name)
    output_pdf = "{0}/{1}.pdf".format(plot_dir, plot_name)
    plt.savefig(output_png, bbox_inches='tight')
    plt.savefig(output_pdf, bbox_inches='tight')
