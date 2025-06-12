#!/usr/bin/python3

import os
import sys
import re
import wrappers
import shutil

year_filter = 0
if len(sys.argv) > 1:
	year_filter = sys.argv[1]

command = 'latex2html -nonavigation -nofootnode -split 0 -lcase_tags -rootdir tmp -mkdir -noaddress -noimages -verbosity 2 -info 0 '

root_directory = '../minutes'

source_directory = root_directory + '/raw'

#stuff to clean out of the minutes
bad_1 = '<#[0-9]+#>'
bad_2 = '<SPAN CLASS="MATH"><tex2html_image_mark>#tex2html_wrap_inline[0-9]+#</SPAN>'

def output_years(dates):
	return "<hr>\n".join([output_year(x, dates[x]) \
				for x in reversed(sorted(dates.keys())) if dates[x]])

def output_year(year, notes):
	q = "<h2>%s</h2>\n<ul class=\"columns\">\n" % year
	for note in sorted(notes):
		q += "<li><a href=\"%s/%s.html\">%s</a></li>\n" % (year, note, note)
	q += "</ul>\n"
	return q

def intro():
	return """<h1>Archive for MITSFS Friday meeting minutes</h1>

<div class="minutes">
<p> If you are really interested at what goes on at our meetings, you can read our latest minutes.</a> If you think those are a fluke and we've got to be more intelligible than that most of the time you can browse through some older minutes, but you're pretty much
doomed.</p>

"""

def is_first_relevant_line(line, date):
	line = line.lower()
	if not line.startswith('<div class="center">'):
		return 0
	
	if line.startswith('<div class="center">mit science fiction society') or \
		line.startswith('<div class="center">84 massachusetts avenue') or \
		line.startswith('<div class="center">cambridge, ma 02139') or \
		line.startswith('<div class="center"><br>') or \
		line.startswith('<div class="center">\n') or \
		line.startswith('<div class="center">mitsfs meeting minutes'):
			return 0
	return 1
	

years = sorted([x for x in os.listdir(source_directory)
			if os.path.isdir(source_directory + '/' + x)])
years.reverse()

all_dates = {}

for year in years:
	dates = [x for x in os.listdir(source_directory + '/' + year) \
							if x.startswith('minutes')]
	if year not in all_dates:
		all_dates[year] = []
	for date in sorted(dates):
		month_day = date[13:18]
		print(year + '/' + date)
		all_dates[year].append(month_day)
		
		if year_filter and year_filter != year:
			continue

		os.system(command + source_directory + '/' + year + '/' + date)			
		input_file = []
		with open("tmp/%s/%s.html" % (date[:-4], date[:-4]), "r") as input:
			input_file = input.readlines()

		os.makedirs(root_directory + "/" + year, exist_ok=True)
		with open("%s/%s/%s.html" % (root_directory, year, month_day), "w") as f:
			write = 0
			f.write (wrappers.head())
			f.write ("<a href=\"/minutes/\">&lt; Minutes Index</a>\n")
			for line in input_file:
				if line == "<br>\n":
					continue
				if line == '</body>\n':
					write = 0
				if write == 0 and is_first_relevant_line(line, date[:-4]):
					write = 1
				if write:
					line = re.sub(bad_1, '', line)
					line = re.sub(bad_2, '+', line)
					f.write(line)
			f.write (wrappers.foot())

with open(root_directory + "/index.html", "w", encoding="utf-8") as f:
	f.write (wrappers.head())
	f.write(intro())
	f.write(output_years(all_dates))
	f.write("</div>")
	f.write (wrappers.foot())

shutil.rmtree("tmp")
