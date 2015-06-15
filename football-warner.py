#!/usr/bin/env python2

import urllib2
import sys
from bs4 import BeautifulSoup

def filter(tag):
	return tag.has_attr('class') and "date" in tag['class']

def dangerous(name):
	dangers = ["liga", "wm", "em", "champions", "pokal", "euro"]
	for danger in dangers:
		if danger in name.lower():
			return True
	return False

def main():

	# usage football-warner.py <name of day (german)> <Starting hour>
	
	day = "Donnerstag"
	hour = 19
	
	if len(sys.argv) > 1:
		day = sys.argv[1]
		hour = int(sys.argv[2])
		

	response = urllib2.urlopen('http://www.fussballgucken.info/fussball-alle-termine')
	html = response.read()
	soup = BeautifulSoup(html)
	
	dangerous_events = []
	
	for div in soup.find_all(filter):
		if day.lower() in  div.contents[0].contents[0].string.lower():
			sibling = div.find_next_sibling()
			while "game" in sibling['id']:
				
				time = sibling.contents[0].contents[0].string
				begin = int(time.split(":")[0])
				matchtype = sibling.contents[0].contents[4].string
				
				if begin >= hour and dangerous(matchtype):
					dangerous_events.append((time,matchtype,day))
				
				sibling = sibling.find_next_sibling() 

	if len(dangerous_events) == 0:
		print "You're good to go!"
	else:
		print "There are potentially evil things at hand!"
		for event in dangerous_events:
			print event[1],"on", event[2], "at", event[0]

if __name__ == "__main__":
	main()
