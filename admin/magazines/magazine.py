#!/usr/bin/python3

import os
import json
import math
from enum import Enum

MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", \
			"Aug", "Sep", "Oct", "Nov", "Dec"]
MAX_ISSUES_PER_ROW = len(MONTHS)

class calTypes(Enum):
	MONTH = "MONTH"
	ISSUES = "ISSUES"

class mag(Enum):
	NAME = "name"
	ALTERNATE_NAMES = "alternate"
	GRID = "grid"
	SEASONS = "season_map"
	YEARS = "years"
	NOTE = "note"
	BOX = "box"
	
class iss(Enum):
	VOLUME = "volume"
	ISSUE = "issue"
	DATE = "date"
	STATUS = "status"
	NOTE = "note"
	
class status(Enum):
	OWNED = "OWNED"
	BOUND = "BOUND"
	MISSING = "MISSING"

STYLE = {status.MISSING.value: "missing", \
			status.OWNED.value: "owned", \
			status.BOUND.value: "bound"}

YEARS = mag.YEARS.value

class location(Enum):
	LIBRARY = "LIBRARY"
	ANNEX = "ANNEX"
	
def loadJson(filename):
	try:
		with open(filename + '.json') as f:
			d = json.load(f)
			return d
	except (OSError, IOError) as e:
		return []
	
def orNone(key, val):
	return key[val] if val in key else None

def orEmpty(key, val):
	return key[val] if val in key else {}
	
"""
Load in the data for the magazine, including following a redirect if there is one
"""
def createMagazine(folder, magazine, root):
	data = loadJson("/".join([root, folder, magazine]))
	if ("redirect" in data):
		data = loadJson("/".join([root, folder, data["redirect"]]))
	if (data):
		return toTable(data)
	return "<p>Unable to locate your magazine. Please go back and try again.</p>"
	
"""
Print the title and generate a table depending on the format specified in the JSON
"""
def toTable(data):
	q = "<h1>" + data[mag.NAME.value]
	if mag.ALTERNATE_NAMES.value in data and data[mag.ALTERNATE_NAMES.value]:
		q += " (aka " + ", ".join(data[mag.ALTERNATE_NAMES.value]) + ")"
	q += "</h1>\n"
	if  mag.NOTE.value in data and data[mag.NOTE.value]:
		q += "<p>(%s)</p>\n" % data[mag.NOTE.value]
	if  mag.BOX.value in data and data[mag.BOX.value]:
		q += "<p>(Annex Box %s)</p>\n" % data[mag.BOX.value]
	
	q += "<table class=\"magazine\">\n"
	if data[mag.GRID.value] == calTypes.MONTH.value:
		q+= monthToTable(data)
	elif data[mag.GRID.value] == calTypes.ISSUES.value:
		q+= issuesToTable(data)
	else:
		q+= notImplementedToTable(data[mag.GRID.value])

	q += "</table>\n"
	q += footer()
	return q

"""
Displays issues that are tagged as per-issue (i.e. not monthly-dated)
"""
def issuesToTable(data):
	biggest = min(max(len(data[YEARS][year]) for year in data[YEARS]), MAX_ISSUES_PER_ROW)
	first_year = int(min(data[YEARS]))
	last_year = int(max(data[YEARS]))

	return "\n".join( [issueYear(year, orEmpty(data[YEARS], str(year)), biggest) \
					for year in range(first_year, last_year + 1) ])

"""
Outputs a year worth of issues. 
Has to do a little bit of pre-crunching to make sure that there aren't more than max
issues per row, and the year row needs to be sized appropriately
"""
def issueYear(year, issues, biggest_row):
	
	row_blocks = [issues[i:i + MAX_ISSUES_PER_ROW] \
					for i in range(0, len(issues), MAX_ISSUES_PER_ROW)]
	tagged_rows = [outputRow(row, biggest_row) for row in row_blocks] \
						if row_blocks else [outputRow([], biggest_row)]
	
	q =  "<tr>\n"
	q += "<th rowspan=\"%i\">%s</th>" % (len(tagged_rows), year)
	q += "</tr>\n<tr>".join(tagged_rows)
	q += "\n</tr>"
	
	return q	

"""
Outputs the issues for the year. Does not output the year itself. 
Takes in the largest row size in the set in case it needs to pad the row out
"""
def outputRow(issues, biggest_row):
	q = ""
	for issue in issues:
		q += "<td class=\"%s\">%s</td>" \
						% (STYLE[issue[iss.STATUS.value]], output_cell(issue))	
	
	#padding in case this row doesn't have as many issues as other rows
	if len(issues) < biggest_row:
		q += "<td"
		if biggest_row - len(issues) > 1:
			q+= " colspan=%s" % (biggest_row - len(issues))	
		q+= "></td>"
	return q

"""
Outputs the HTML for the cell contents for an indvidual issue
"""
def output_cell(issue):
	lines = []
	if iss.ISSUE.value in issue:
		number = "#%s" % issue[iss.ISSUE.value]
		if "volume" in issue and issue["volume"]:
			number = "V%s " % issue[iss.VOLUME.value] + number
		lines.append(number)
	if iss.DATE.value in issue:
		date = issue[iss.DATE.value]
		if date.startswith("mid"):
			date = date[3:]
		if date.startswith("late"):
			date = date[4:]
		lines.append(date)
	if iss.NOTE.value in issue:
		lines.append("(%s)" % issue[iss.NOTE.value])
	return "<br>".join(lines)
		
"""
Displays issues that are tagged as per-month
Includes a header with all the months in it
"""
def monthToTable(data):
	first_year = int(min(data[YEARS]))
	last_year = int(max(data[YEARS]))

	q = "<tr>\n"
	q += "<th>Year</th>\n<th>"
	q += "</th>\n<th>".join(MONTHS)
	q += "</th>\n</tr>\n"
	
	q += "\n".join([monthYear(year, \
							  orEmpty(data[YEARS], str(year)), \
							  orEmpty(data, mag.SEASONS.value)) \
					for year in range(first_year, last_year + 1) ])

	return q

"""
Outputs a year worth of issues. 

If any issues in the year have a "mid" or "late" prefix, outputs them into a 
second/third row for the year
"""
def monthYear(year, issues, seasons):
	q = "<tr>\n"

	#find arrays with mid issues and pull them into a second array. 
	#making the assumption that we won't have "mid" attached to multiple month or
	#season scenarios
	mid_issues = [x for x in issues if x[iss.DATE.value].startswith("mid")]
	late_issues = [x for x in issues if x[iss.DATE.value].startswith("late")]
	issues = [x for x in issues if not x[iss.DATE.value].startswith("mid") \
								and not x[iss.DATE.value].startswith("late")]
	rows = ""
	if mid_issues:
		rows = " rowspan=2" 
	if late_issues:
		rows = " rowspan=3"
	
	q += "<th%s>%s</th>" % (rows, year)
	if (issues is None):
		q += "<td colspan=12></td>"
		return q
	q += processMonths(issues, seasons)
	if mid_issues:
		q += "<tr>%s</tr>" % processMonths(mid_issues, seasons)
	if late_issues:
		q += "<tr>%s</tr>" % processMonths(late_issues, seasons)
		
	q += "</tr>\n"
	return q	

"""
Outputs a row of months (without the row wrapper). 

The trick here is that you need to track the overall progress against the calendar
so that you properly line up the gaps.

Supports multiple months separated by hyphens, though you have to spell them all out.
Supports seasons as aliases for strings of months (which means you can hack for certain weird trickery). Ignores the "mid" and "late" prefix.
"""

def processMonths(issues, seasons):
	
	#this is the pointer into the month array to keep track of where we are
	current_month_position = 0
	q = ""
	
	for issue in issues:	
		issue_value = issue[iss.DATE.value]
		
		#A lot of magazines do seasons and the month mapping varies. So we declare
		#that in the configuration and map to the issues
		if issue_value in seasons:
			issue_value = seasons[issue_value]
		if issue_value.startswith("mid"):
			issue_value = issue_value[3:]	
		if issue_value.startswith("late"):
			issue_value = issue_value[4:]	
		issue_months = issue_value.split("-")
		
		#See if the current issue matches up with the calendar. If not, pad until
		# we get there.
		month_offset = 0
		while current_month_position < len(MONTHS) and \
				MONTHS[current_month_position] != issue_months[0]:
			month_offset += 1
			current_month_position += 1
		if current_month_position >= len(MONTHS):
			q += "<td>Bad month specified: %s</td>" % issue_months[0]
			return q
		
		if month_offset > 1:
			q += "<td colspan=%s></td>" % month_offset 
		elif month_offset > 0:
			q += "<td></td>"

		#now span the issue to the months specified	and output a cell that big	
		issue_columns = 0
		for month in issue_months:
			if month != MONTHS[current_month_position]:
				q += "<td>Bad month specified: %s</td>" % month
				return q
			issue_columns += 1
			current_month_position += 1;		
		
		colspan = ""
		if issue_columns > 1:
			colspan = " colspan=%s" % issue_columns
		q += "<td class=\"%s\"%s>%s</td>" % \
				(STYLE[issue[iss.STATUS.value]], colspan, output_cell(issue))
	
	#If we run out of issues, and there's more calendar, pad the rest
	if current_month_position < len(MONTHS):
		q += "<td"
		if len(MONTHS) - current_month_position > 1:
			q+= " colspan=%s" % (len(MONTHS) - current_month_position)	
		q+= "></td>"

	return q


"""
Outputs a footer showing the color legend
"""
def footer():
	q = '<p><span class="' + STYLE[status.MISSING.value] + \
		'">Missing</span>&nbsp;&nbsp;&nbsp;&nbsp;' + \
		'<span class="' + STYLE[status.OWNED.value] + \
		'">Owned</span>&nbsp;&nbsp;&nbsp;&nbsp;' + \
		'<span class="' + STYLE[status.BOUND.value] + \
		'">Bound</span></p>\n'
	return q
"""
Just for debugging
"""
def notImplementedToTable(schedule):
	q = "<table class=\"magazine\">\n"
	q += "<tr><td>" + schedule + " form not implemented</tr></td>\n"
	q += "</table>\n"
	return q
	
