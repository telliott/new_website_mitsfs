#!/usr/bin/python3
import os
import re
import html
import json
from math import ceil

SECTIONS = {"library_front": "The Big Guns",
			"library_small": "Small-Format Magazines",
			"library_large": "Large-Format Magazines",
			"library_xl": "Extra-Large-Format Magazines",
			"annex": "Magazines in the Annex",
			"annex_foreign": "Foreign Magazines in the Annex",
			"one_offs.json": "One-Off Issues of Larger Publications (in the Annex)",
			"foreign_one_offs.json": "One-Off Issues of Foreign Publications (in the Annex)"
			}
			
def loadJson(filename):
	try:
		with open(filename) as f:
			d = json.load(f)
			return d
	except (OSError, IOError) as e:
		return []
	
"""
Loops through the categories and outputs a table for each
"""
def createFrontpage(root, link_template):
	q = "<h1>The MITSFS Magdex</h1>\n"
	q += "\n<hr>\n".join([tableOfContents(section, root, link_template) for section in SECTIONS.keys()])
	return q
	
"""
Finds all the filenames in a directory that end with .json and generates a table to reflect them
"""
def tableOfContents(section, root, link_template):
	magazines = []
	raw_display = section.endswith(".json")
	if raw_display:
		magazines = loadJson("/".join([root, section])).get("issues", [])
	else:
		directory = root + section
		magazines = sorted([x for x in os.listdir(directory) if x.endswith(".json")], \
							key=str.casefold)

	if (not magazines):
		return "";	
	
	q = "<h2>%s</h2>\n" % SECTIONS[section]
	q += "<ul class=\"columns\">"
	if raw_display:
		q += outputTextColumn(magazines)
	else:	
		q+= outputColumn(section, magazines, link_template)
	q+= "</ul>"

	return q

"""
Creates list of magazines with links
"""
def outputColumn(section, magazines, link_template):
	return "\n".join([create_entry(link_template, section, mag) for mag in magazines])

"""
Creates the list for unlinked magazines
"""
def outputTextColumn(magazines):
	q = ""
	for mag in magazines:
		text = "%s (%s)" % (mag.get("name", ""), mag.get("issue", ""))
		if mag["note"]:
			text += " - %s" % mag["note"]
		if mag["box"]: 
			text += " (Box %s)" % mag["box"]
		q += "<li>%s</li>" % text
	return q

"""
Strip off the suffix and turn underscores into spaces for the display name.
Fill in the template URL with the magazine info and return the list item
"""
def create_entry(link_template, section, mag):
	name = re.sub("\..*", "", mag)
	link = re.sub("\[SECTION\]", html.escape(section), link_template)
	link = re.sub("\[MAG\]", html.escape(name), link)
	
	name = re.sub("_", " ", name)

	return "<li><a href=\"%s\">%s</a></li>" % (link, name.strip())
