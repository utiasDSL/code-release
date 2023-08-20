'''Data format utility functions.

'''
import os
import json
import pandas as pd
import ast

from column_ids import ColumnIDs


def drop_columns(sheet : str, columns_to_drop : list, conf : str) -> None:
	# Open sheet
	print('Opening', sheet)
	with open(sheet) as json_file:
		parsed_json = json.load(json_file)
		parsed_json = json.loads(parsed_json)
	df = pd.DataFrame(parsed_json)
	
	# Drop columns
	columns_to_drop = [i - 1 for i in columns_to_drop]
	columns_to_drop.sort(reverse=True)

	for i in columns_to_drop:
		df.drop(df.columns[i], axis=1, inplace=True)
	
	# Rename headers
	if conf in ['CDC', 'ICRA']:
		df = df.rename(columns={'Code Link': 'With Code'})
		df = df.rename(columns={'Crossref Citations' : 'Citations'})
	else:
		df = df.rename(columns={'Github' : 'With Code'})

	# Drop rows with -1 citations
	df.drop(df[df.Citations == -1].index, inplace=True)

	# Swap order of With Code and Citations
	new_order = ['Year', 'Citations', 'With Code']
	df = df.reindex(columns=new_order)

	# Set With Code column to True False basis
	if conf in ['CDC', 'ICRA']:
		df['With Code'] = [True if 'github' in str(row).lower() else False for row in df['With Code']] 
	else:
		df['With Code'] = [True if len(ast.literal_eval(row)) > 0 else False for row in df['With Code']]

	# Reformat years if conf is IEEE
	if conf in ['CDC', 'ICRA']:
		df['Year'] = [str(row)[-4:] for row in df['Year']]

	print('-- Saving...')
	df.to_csv('.' + sheet.rsplit('.')[1] + '_code.csv', index=False, encoding='utf-8')


def merge(spreadsheets : list, conf : str) -> None:
	df = []

	for sheet in spreadsheets:
		sheet = '.' + sheet.rsplit('.')[1] + '_code.csv'
		print('Opening', sheet)
		df_tmp = pd.read_csv(sheet)

		print(df_tmp.loc[df_tmp['Citations'].idxmax()])
		print(df_tmp.loc[df_tmp['Citations'].idxmin()])

		df.append(df_tmp)

	# Merge sheets
	for i in range(1, len(df)):
		df[0] = pd.concat([df[0], df[i]], ignore_index=True)

	# Save sheet
	print('-- Saving...')
	df[0].to_csv('./' + conf + '/' + 'ALL_DATA.csv', index=False)


def merge_sheets(spreadsheets, conf):
	columns_to_drop = [ColumnIDs.CONFERENCE, ColumnIDs.TITLE, ColumnIDs.AUTHOR, 
		    ColumnIDs.KEYWORD, ColumnIDs.BENCHMARK, ColumnIDs.RESULT, 
			ColumnIDs.STAR, ColumnIDs.FORK, ColumnIDs.CIT_OVER_TIME]
	for i in range(len(spreadsheets)):
		spreadsheets[i] = './' + conf + '/' + spreadsheets[i]

	for sheet in spreadsheets:
		if conf in ['CDC', 'ICRA']:
			columns_to_drop = columns_to_drop[:-1]
		drop_columns(sheet, columns_to_drop, conf)

	# Merge all years into one csv
	merge(spreadsheets, conf)

	for sheet in spreadsheets:
		os.remove('.' + sheet.rsplit('.')[1] + '_code.csv')
