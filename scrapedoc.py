from urllib2 import urlopen
from bs4 import BeautifulSoup
import unittest
import re


def choose_site(url, ids):
	webpage = urlopen(url)
	soup = BeautifulSoup(webpage)
	product = soup.select("body")
	return product

def choose_price(url, ids):
	webpage = urlopen(url)
	price = {}
	soup = BeautifulSoup(webpage)
	ids = ids.split(',')
	for specific_id in ids:
		print specific_id
		if specific_id:
			product = soup.select("#%s" % (specific_id))
			prices = re.search("\$\d+", str(product))
			if prices:
				price[specific_id] = prices.group()
	return price

