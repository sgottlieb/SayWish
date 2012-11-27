from urllib2 import urlopen
import urllib, cStringIO
from bs4 import BeautifulSoup
from PIL import Image
from StringIO import StringIO
from model import SESSION as db_session
import model
import os
import requests
import unittest
import re


unwanted_titles = ['Shop', 'Clothing', 'Shoe', 'Bag', 'Accessories',
'Designer', 'Exclusives', 'Workwear', 'Wedding',  'Essentials','Denim', 'Dresses', 
'Leather', 'Legging', 'Lingerie', 'Maternity', 'Pant', 'Short', 'Skirt', 'Suit',
'Swimwear', 'Vest', 'Boot','Pump', 'Sandal','Backpacks','Clutch', 'Cosmetic',  'Pouches','Satchel', 
'Tote', 'Wallet', 'Accessories', 'Jewelry', 'Belt', 'Book',  'Eyewear', 'Glove', 'Hair','Hat',
'Hosiery', 'Keychain', 'Product', 'Tech', 'Umbrella','Sale', 'Lookbook',  'Account', 'Order',  
'shipping', 'zipcode', 'ground shipping', "what's new", "wish list", 
'holiday', 'jacket' 'coat', 'New ', "Editor",'Holiday Gift Boutique', 'Clothing', 'Denim',
'Dresses', 'Romper','Boutiques',  'Leather', 'Leggings', 'Lingerie', 
'Loungewear','Yoga', 'Maternity', 'Pants', 'Shorts', 'Skirts', 'Gifts', 'Hosiery', 'Keychain', 
'Scarves', 'Wrap', 'Percent', 'Feature', 'Account', 'Order', 'Review', 'List' ]

def get_host(url):
	host_name = re.search('http://\w+.(\w+).', str(url)).group(1)
	return host_name

def check_host(url):
	host_name = get_host(url)
	in_db = model.Website.search(host_name)
	if in_db:
		return in_db
	else: 
		return None

def open_site(url):
	webpage = urlopen(url)
	soup = BeautifulSoup(webpage)
	webpage.close()
	return soup


def split_class(classes):
	class_list = []
	print "here"
	classes = str(classes).split(',')
	for specific_class in classes:
		if specific_class:
			class_list.append(specific_class)
	return class_list

def first_time(url, classes):
	best_div = {}
	class_list = split_class(classes)
	title_list = []
	soup = open_site(url)
	for specific_class in class_list:
		product = soup.select(".%s" % (specific_class))
		title = get_titles(product)
		if title:			
			best_div[specific_class]= title
	return best_div

def get_titles(product):
	title_list = []
	title_matches = re.finditer(">\s*(\w+?.*?\w*?)\s*<", str(product))
	titles = [match_obj.group(1) for match_obj in title_matches]
	for title in titles:
		if wanted_title(title) and title not in title_list:
			title_list.append(title)
	return title_list

def wanted_title(title):
	for unwanted in unwanted_titles:
		if unwanted.lower() in title.lower():
			return False
	return True


## FIX PRICE BUG, NOT IN THE RIGHT LOOP
def find_best_price_div(url, class_list):
	similar_price = []
	price_divs = {}
	soup = open_site(url)
	for specific_class in class_list:
		product = soup.select(".%s" % (specific_class))
		price_list = find_prices(product, specific_class)
		for price in price_list:
			if price and price not in similar_price:
				similar_price.append(price)
		price_divs[specific_class] = price_list
	return price_divs

def price_check(url, specific_class):
	similar_price = []
	soup = open_site(url)
	product = soup.select(".%s" % (specific_class))
	price_list = find_prices(product, specific_class)
	for price in price_list:
		if price and price not in similar_price:
			similar_price.append(price)
	return similar_price

def find_prices(product, specific_class):
	price_options = ["\$\d+.?\d*", "\d+.?\d*?\s?USD?"]
	price_list = []
	for price_type in price_options:
		prices = re.findall("%s" %(price_type), str(product))
		for price in prices:
			if price not in price_list and price:
				price_list.append(price)
	if len(price_list) > 1:
		price_list.sort()
	return price_list


def find_images(url):
	images= {}
	soup = open_site(url)
	for image in soup.findAll("img"):
		if image["src"].lower().startswith("http"):
			resp = requests.get("%(src)s" % image)
			i = Image.open(StringIO(resp.content))
			if i.size[0] > 200 and i.size[1] > 200:
				i.save('./static/img/productImage' , 'jpeg')
				return image["src"]
