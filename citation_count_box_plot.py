'''Plotting functions for box plots

'''
import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import seaborn as sns
import pandas as pd
import tikzplotlib


# Fixes AttributeError when using a legend in matplotlib for tikzplotlib
from matplotlib.lines import Line2D
from matplotlib.legend import Legend
Line2D._us_dashSeq    = property(lambda self: self._dash_pattern[1])
Line2D._us_dashOffset = property(lambda self: self._dash_pattern[0])
Legend._ncol = property(lambda self: self._ncols)


def calc_percentage(minuend, subtrahend, denom):
    if abs(denom) <= 1e-8:
        return float('inf')
    return (minuend - subtrahend) / denom * 100.0


def percentual_change(percentages):
    percentage_diff = []
    for i in range(len(percentages)-1):
        percentage_diff.append(calc_percentage(percentages[i + 1], percentages[i], percentages[i]))

    return percentage_diff


def print_percentages(stats_code, stats_no_code, name=''):
    percent_no_code = percentual_change(stats_no_code)
    percent_code = percentual_change(stats_code)
    print('{} NO code: {}'.format(name, stats_no_code))
    print('Changes: ', ['{:.2f} %'.format(percent) for percent in percent_no_code])
    print('{} W/ code: {}'.format(name, stats_code))
    print('Changes: ', ['{:.2f} %'.format(percent) for percent in percent_code])
    diff_percentage_quartile = [calc_percentage(percent_code[i], percent_no_code[i], percent_no_code[i]) for i in range(len(percent_no_code))]
    print('diff Changes: ', ['{:.2f} %'.format(percent) for percent in diff_percentage_quartile])


def add_percentile_labels(ax, percentile_name='Median', fmt='.1f'):
    # adapted from https://stackoverflow.com/a/63295846 by Christian Karcher
    no_code = []
    code = []
    
    # Get the lines and boxes in the box plot
    lines = ax.get_lines()
    boxes = [c for c in ax.get_children() if type(c).__name__ == 'PathPatch']
    lines_per_box = int(len(lines) / len(boxes))

    # Determine the elements to loop over (lines for medians, boxes for quartiles)
    if percentile_name == 'Median':
        plot_elements = lines[4:len(lines):lines_per_box]
    elif percentile_name == 'Third Quartile':
        plot_elements = boxes
    else:
        raise NotImplementedError
    
    for plot_element in plot_elements:
        # Determine x and y data for median or quartile
        if percentile_name == 'Median':
            x, y = (data.mean() for data in plot_element.get_data())
            foreground = plot_element.get_color()
        elif percentile_name == 'Third Quartile':
            top_left = plot_element.get_path().vertices[2, :]
            top_right = plot_element.get_path().vertices[3, :]
            y = top_left[1]
            x = (top_right[0] - top_left[0]) / 2.0 + top_left[0]
            foreground = plot_element.get_edgecolor()
        else:
            raise NotImplementedError

        # Alternate between without OSC and with OSC data
        if len(code) >= len(no_code):
            no_code.append(y)
        else:
            code.append(y)
        
        # Add text for percentile
        text = ax.text(x, y, f'{y:{fmt}}', ha='center', va='center', 
                       fontweight='bold', color='white')
        
        # Create colored border around white text for contrast
        text.set_path_effects([
            path_effects.Stroke(linewidth=3, foreground=foreground),
            path_effects.Normal(),
        ])
    
    return code, no_code
        

def citation_count_w_wo_code(conf, cfg):
    add_statistics = cfg['ADD_STATISTICS']

    # Print conference name
    print('Conference {}'.format(conf))

    # Set paths for data and plotting
    csv_file_name = conf + '/ALL_DATA.csv'
    figure_output_file = 'plots/Code Availability vs Citations in {} Box Plot.'.format(conf)

    # Read CSV file
    data_plt = pd.read_csv(csv_file_name)

    # The number of years for plotting the data
    years = list(set(data_plt.Year))  # get the years
    reversed_years = years[::-1]  # reverse order of years

    # Create box plots
    ax = sns.boxplot(x='Year', y='Citations', hue='With Code', data=data_plt, showfliers=False, order=reversed_years) 

    # Set labels
    ax.set_xticklabels(['{} ({})'.format(reversed_years[0] + 1 - year, year) for year in reversed_years])
    ax.set_xlabel('Years since Publication (from {})'.format(reversed_years[0] + 1))
    ax.set_ylabel('Semantic Scholar Citations')
    plt.title(conf)

    if add_statistics:
        percentile_names = ['Median', 'Third Quartile']
        for percentile_name in percentile_names:
            print(percentile_name)
            # label the median and third quartiles on the plot
            code, no_code = add_percentile_labels(ax, percentile_name=percentile_name)
            # print changes in percentile for publications with and without OSC over the years 
            print_percentages(code, no_code, name=percentile_name)

    # Create tikz figure and save PNG
    tikzplotlib.clean_figure()
    tikzplotlib.save(figure_output_file + 'tex')
    plt.savefig(figure_output_file + 'png')
    plt.show()
