#!/usr/bin/python3
import os
import re
import html
import json
from math import ceil

table_keys = ['Author', 'Title', 'Year', 'Reviewer', 'Reviewed', 'Publisher']

def cell_value(data, key):
	if key == 'Title':
		return "<a href=\"review/%s.html\">%s</a>" % (data['filename'], data['Title'])
	else:
		return data[key] if key in data else ""
 
def createFrontpage(metadata):
	q = intro()
	q += "<table class=\"striped\">\n"
	q += "<thead>%s</thead>\n" % get_head_row()
					
	q += "<tbody>%s</tbody>\n" % get_rows(metadata)
	q += "</table>\n"
	return q

def get_head_row():
	return "<tr>%s</tr>" % "\n".join(["<th>%s</th>" % key for key in table_keys])


def get_rows(metadata):
	return "\n".join([get_row(row) for row in \
				sorted(metadata, key=lambda d: d['Author'].lower())])
	
def get_row(metadata_row):
	
	return "<tr>%s</tr>" % \
		"\n".join(["<td>%s</td>" % cell_value(metadata_row, key) for key in table_keys])


def intro():
      return """<h1>Reviews</h1>
      
<p>Here's a place for reviews by MITSFS members.</p>

<p>If you're a MITSFS member and you'd like to review a book, please do!  Read a few of the other reviews to get a sense of the style (e.g. we're more interested in what sort of a book it is, rather than assigning it a good/bad rating).  Although there's a preference for new books, it's fine to review older books, especially when it's an author that not everybody in the world reads.  An interesting and well-explained opinion on any book, even one already reviewed, is always welcome.  When you're done, email your review to
<strong><a href="mailto:kvetchcomm@mit.edu">kvetchcomm@mit.edu</a></strong>.</p>"""


