'''Main plotting script

Run as:

    $ python3 main.py

'''
import yaml
import os


from analyze import historical_papers, stars_vs_citations
from citation_count_box_plot import citation_count_w_wo_code
from json_to_csv import merge_sheets


def main(config):
    conferences = config['CONFERENCES']
    years = config['YEARS']
    spreadsheets = ['{}_DATA.json'.format(year) for year in years]

    for conf in conferences:
        # Figure 2 
        historical_papers(conf, spreadsheets.copy(), years, config)
        # Figure 3
        merge_sheets(spreadsheets.copy(), conf)
        citation_count_w_wo_code(conf, cfg)

    # Figure 4
    stars_vs_citations('NeurIPS', spreadsheets.copy(), config)


if __name__ == '__main__':
    # Configure correct function args with .yaml
    with open('config.yaml') as f:
        cfg = yaml.load(f, Loader=yaml.FullLoader)

    # Create folder for plots
    if not os.path.isdir(cfg['SAVE_DIR']):
        os.makedirs(cfg['SAVE_DIR'])

    main(cfg)
