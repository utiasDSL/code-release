from enum import IntEnum, unique


@unique
class ColumnIDs(IntEnum):
	'''A class that creates ids for relevant columns in the spreadsheet.'''

	CONFERENCE = 1
	YEAR = 2
	TITLE = 3
	AUTHOR = 4
	KEYWORD = 5
	BENCHMARK = 6
	RESULT = 7
	CODE = 8
	STAR = 9
	FORK = 10
	CITATION = 11
	CIT_OVER_TIME = 12
    