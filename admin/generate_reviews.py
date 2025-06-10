#!/usr/bin/python3

import os
import re
from reviews import reviewpage
from reviews import frontpage
import wrappers

review_root = "../reviews"
text_root = review_root + "/raw"
output_root = review_root + "/review"

#URL to reviews (tells the frontpage how to construct a review link).
review_url = "review/[REVIEW].html"


# Path to root folder where review txt files are		
os.makedirs(output_root, exist_ok=True)

reviews = [x for x in os.listdir(text_root) if x.endswith(".txt")]
review_list = []
for review in reviews:
	print(review)
	
	with open(text_root + '/' + review, 'r', encoding="utf-8") as f:
		metadata = {'filename': review[:-4]};
		review_text = []
		current_line = []
		in_header = 1
		for line in [line.rstrip() for line in f.readlines()]:
			if len(line) == 0 and in_header:
				in_header = 0
				continue
			
			if in_header:
				result = re.split(": +", line, 1)
				if result[0] in ("Authors", "Director"):
					result[0] = "Author"
				metadata[result[0]] = result[1]
			elif len(line) == 0:
				if current_line:
					review_text.append(" ".join(current_line))
					current_line = []
			else:
				current_line.append(line)	
				
		if current_line:
			review_text.append(" ".join(current_line))
		
		
		with open("%s/%s.html" % (output_root, review[:-4]), "w", encoding="utf-8") as f:
			f.write (wrappers.head())
			f.write ("<a href=\"/reviews/\">&lt; Review Index</a>\n")
			f.write (reviewpage.createReview(metadata, review_text))
			f.write (wrappers.foot())

		review_list.append(metadata)

		
with open(review_root + "/index.html", "w", encoding="utf-8") as f:
	f.write (wrappers.head())
	f.write (frontpage.createFrontpage(review_list))
	f.write (wrappers.foot())

