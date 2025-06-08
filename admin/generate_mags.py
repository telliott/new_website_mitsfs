#!/usr/bin/python3
import os
import urllib.parse
import json
import sys
sys.path.append("..")
from magazines import magazine
from magazines import frontpage
import wrappers

#URL to magazines (tells the frontpage how to construct a magazine link). Actual mag link 
#will be substituted into the [] sections
magazine_url = "[SECTION]/[MAG].html"

# path to magdex
magdex_root = "../magdex"

# Path to root folder where magazine folders are		
magazine_root = magdex_root + "/magazines"



with open(magdex_root + "/index.html", "w") as f:
	f.write (wrappers.head())
	f.write (frontpage.createFrontpage(magazine_root + "/", magazine_url))
	f.write (wrappers.foot())


for section in [x for x in frontpage.SECTIONS.keys() if not x.endswith(".json")]:
	directory = magazine_root + "/" + section
	magazines = sorted([x for x in os.listdir(directory) if x.endswith(".json")], \
							key=str.casefold)
	os.makedirs(magdex_root + "/" + section, exist_ok=True)
	for mag in magazines:
		print(mag)
		#strip .json off the magazine
		mag = mag[:-5]
		with open(magdex_root + "/%s/%s.html" % (section, mag), "w") as f:
			f.write (wrappers.head())
			f.write ("<a href=\"/magdex/\">&lt; Magazine Index</a>\n")
			f.write (magazine.createMagazine(section, mag, magazine_root))
			f.write (wrappers.foot())


