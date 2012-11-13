from urllib2 import urlopen
import urllib, cStringIO
from bs4 import BeautifulSoup
from PIL import Image
from StringIO import StringIO
import os

import requests
import unittest
import re

def open_site(url):
	webpage = urlopen(url)
	soup = BeautifulSoup(webpage)
	return soup


def first_time(url, ids):
	soup = open_site(url)
	best_div = {}
	ids = ids.split(',')
	for specific_id in ids:
		if specific_id:
			product = soup.select("#%s" % (specific_id))
			prices = re.findall("\$\d+.?\d*", str(product))
			title_matches = re.finditer(">\s*(\w\w+\s*?\w*?)\s*?<", str(product))
			titles = [match_obj.group(1) for match_obj in title_matches]
			if prices or titles:
				best_div[specific_id]=[titles, prices]
	print best_div
	return best_div

def find_images(url):
	images= {}
	soup = open_site(url)
	for image in soup.findAll("img"):
		if image["src"].lower().startswith("http"):
			resp = requests.get("%(src)s" % image)
			i = Image.open(StringIO(resp.content))
			if i.size[0] > 200 and i.size[1] > 200:
				i.show()
				img_id = image['id']
				i.save('static/img/%s' % img_id, "JPEG")
				images[image['id']]= i
	return images
