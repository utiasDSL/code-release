'''Plotting functions for histograms and stars-vs-citations ellipses

'''
import matplotlib.pyplot as plt
import numpy as np
from sympy import *
from sklearn.covariance import MinCovDet
import tikzplotlib
import json
import pandas as pd


# Fixes AttributeError when using a legend in matplotlib for tikzplotlib
from matplotlib.lines import Line2D
from matplotlib.legend import Legend
Line2D._us_dashSeq    = property(lambda self: self._dash_pattern[1])
Line2D._us_dashOffset = property(lambda self: self._dash_pattern[0])
Legend._ncol = property(lambda self: self._ncols)


from column_ids import ColumnIDs


def get_conf_year(file_name):
    ''' Returns the conference year from a file name, e.g., 
            extracts 2016 from '2016_DATA.json' '''
    return int(''.join(filter(str.isdigit, file_name)))

    
def historical_papers(conf, spreadsheets, years, cfg):
    ''' Returns number of papers with and without code over the years 
        
        Args:
            None
    '''	
    output_folder = cfg['SAVE_DIR']
    plt_filename = output_folder + 'Percentage of Papers with Code at ' + conf

    for i in range(len(spreadsheets)):
        spreadsheets[i] = './' + conf + '/' + spreadsheets[i]

    ## Define data
    with_code = []
    without_code = []
    tot_papers = []

    for sheet in spreadsheets:
        ## Open spreadsheet
        try:
            with open(sheet) as json_file:
                parsed_json = json.load(json_file)
                parsed_json = json.loads(parsed_json)
            df = pd.DataFrame(parsed_json)
        
            code_key = df.columns[ColumnIDs.CODE - 1]
        except:
            print('ERROR: file {} does not exist'.format(sheet))
            return
            
        print('Opened:', sheet)
        
        with_code_num = 0
        without_code_num = 0

        last_row = len(df.index)
        year_tot = 0
        
        for r in range(last_row):			
            year_tot += 1
            
            val = df[code_key].iloc[r]
            try:
                list_value = val.splitlines()
            except:
                without_code_num += 1
                continue
                
            found_code = False
            
            if conf in ['CDC', 'ICRA']:
                for item in list_value:
                    if 'github.com' in item.lower():
                        found_code = True
                        break
            else:
                for item in list_value:
                    if item != 'None' and item != '[]':
                        found_code = True
            
            if found_code:
                with_code_num += 1
            else:
                without_code_num += 1

        with_code.append(with_code_num)
        without_code.append(without_code_num)
        tot_papers.append(year_tot)
        year_tot = 0
    
    x_axis = np.arange(len(years))
    
    # Graph double bar chart across time
    plt.bar(x_axis +0.2, with_code, width=0.4, label='Papers With Code', color='green')
    plt.bar(x_axis -0.2, tot_papers, width=0.4, label='Total Papers', color='grey')
    
    for i in range(len(years)):
        with_code_txt = str(round(with_code[i] / tot_papers[i] * 100, 1)) + '%'
        plt.text((x_axis +0.2)[i], with_code[i] + 1, with_code_txt, ha='center', fontsize=12)
        plt.text((x_axis -0.2)[i], tot_papers[i] + 1, tot_papers[i], ha='center', fontsize=12)
    
    plt.xticks(x_axis, years, fontsize=12)
    plt.yticks(fontsize=12)
    plt.legend(fontsize=12)
    
    plt_title = 'Percentage of Papers with Code at ' + conf
    plt.title(plt_title, fontsize=18)
    plt.xlabel('Conference Year', fontsize=14)
    plt.ylabel('Number of Papers', fontsize=14)

    tikzplotlib.save(plt_filename + '.tex')
    plt.savefig(plt_filename + '.png')
    plt.show()


def plot_ellipsoid(mean, covariance, s, circle, line, year, color):
    eig_values, eig_vectors = np.linalg.eig(s * covariance)

    area = np.pi * np.sqrt(eig_values[0] * eig_values[1])
    
    print('Area {}: {:.2f}'.format(year, area))

    if max(eig_values) > eig_values[0]:
        eig_values = np.array([eig_values[1], eig_values[0]]).T
        eig_vectors = np.array([eig_vectors[:, 1], eig_vectors[:, 0]])

    rotated_ellipse = eig_vectors @ np.diag(np.sqrt(eig_values)) @ np.vstack((circle[0], circle[1]))
    plt.plot(rotated_ellipse[0, :] + mean[0], rotated_ellipse[1, :] + mean[1], color + '-',
            label=year)

    rotated_line = eig_vectors @ np.diag(np.sqrt(eig_values)) @ np.vstack((line[0], line[1]))
    slope = np.abs(rotated_line[1, -1]/ rotated_line[0, -1])

    print('Slope {}: {}'.format(year, slope))
    plt.plot(rotated_line[0, :] + mean[0], rotated_line[1, :] + mean[1], color + '-')

    plt.plot(mean[0], mean[1], color + 'x')
    
    return area, slope
    
    
def stars_vs_citations(conf, spreadsheets, cfg):
    ''' Plots a scatter plot of github stars versus citations for papers
        with github code.
    '''
    output_folder = cfg['SAVE_DIR']
    plt_filename = output_folder + 'Github Stars vs Paper Citations in ' + conf

    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    
    confidence = 0.99
    s = -2 * np.log(1 - confidence)

    angle = np.linspace(0, 2 * np.pi)

    areas = []
    slopes = []

    circle = [np.cos(angle), np.sin(angle)]
    line = [np.array([-1, 1]), np.array([0, 0])]

    for i in range(len(spreadsheets)):
        spreadsheets[i] = './' + conf + '/' + spreadsheets[i]
            
    for i, sheet in enumerate(spreadsheets):	
        ## Define data
        paper_stars = []
        paper_citations = []
        paper_titles = []
        
        ## Open spreadsheet
        try:
            with open(sheet) as json_file:
                parsed_json = json.load(json_file)
                parsed_json = json.loads(parsed_json)
            df = pd.DataFrame(parsed_json)
        
            citation_key = df.columns[ColumnIDs.CITATION - 1]
            star_key = df.columns[ColumnIDs.STAR - 1]
            title_key = df.columns[ColumnIDs.TITLE - 1]
        except:
            print('ERROR: file {} does not exist'.format(sheet))
            return

        print('Opened:', sheet)	
        year = get_conf_year(sheet)
        last_row = len(df.index)
        
        for r in range(last_row):			
            val = df[star_key].iloc[r]
            val2 = df[citation_key].iloc[r]
            
            if val2 == -1 or val == -1:
                continue
                
            # Store the number of citations
            paper_citations.append(val2)
            
            # Store the number of stars
            paper_stars.append(val)
            
            # Store paper title
            val3 = df[title_key].iloc[r]
            paper_titles.append(val3)

        data = np.vstack((np.array(paper_stars), np.array(paper_citations))).T
        result = MinCovDet(assume_centered=False).fit(data)

        cov = result.covariance_
        mean = result.location_

        area, slope = plot_ellipsoid(mean, cov, s, circle, line, year, colors[i])
        areas.append(area)
        slopes.append(slope)

    areas = np.array(areas[::-1])
    diff_percentages_area = np.diff(areas) / areas[:-1] * 100.0
    print('diff changes area: ', ['{:.2f} %'.format(percent) for percent in diff_percentages_area])

    slopes = np.array(slopes[::-1])
    diff_percentages_slope = np.diff(slopes) / slopes[:-1] * 100.0
    print('diff changes slope: ', ['{:.2f} %'.format(percent) for percent in diff_percentages_slope])

    plt.legend(fontsize=12)

    plt.xlabel('Github Stars', fontsize=14)
    plt.ylabel('Semantic Scholar Citations', fontsize=14)

    plt.xlim([0, 500])
    plt.ylim([0, 500])

    plt.title(conf)

    tikzplotlib.save(plt_filename + '.tex')
    plt.savefig(plt_filename + '.png')
    plt.show()
