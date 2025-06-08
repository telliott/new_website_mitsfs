#!/usr/bin/python3

def head(): 
	with open('page_template.html', 'r') as file:
		file_content = file.read()
	results = file_content.split("PAGE GOES HERE", 1)
	return results[0]

def foot():
	with open('page_template.html', 'r') as file:
		file_content = file.read()
	results = file_content.split("PAGE GOES HERE", 1)
	return results[1]

