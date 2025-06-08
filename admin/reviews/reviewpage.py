#!/usr/bin/python3

import os
import json
import math



"""
Load in the data for the magazine, including following a redirect if there is one
"""
def createReview(metadata, text):
	
	
	
	q = "<p><span class=\"review-title\">%s</span> <span class=\"review-author\">(%s, %s)</span></p>\n" % (metadata["Title"], metadata["Author"], metadata["Year"])
	q += "<p class=\"review-reviewer\">Reviewed by %s</p>\n" % metadata["Reviewer"]
	q += "\n".join(["<p>%s</p>" % line for line in text])
	return q