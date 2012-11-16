from urllib2 import urlopen
import urllib, cStringIO
from bs4 import BeautifulSoup
from PIL import Image
from StringIO import StringIO
import os
import requests
import unittest
import re

unwanted_titles = ['Shop All', 'Clothing', 'Shoes', 'Bags', 'Accessories', 'Designer Boutique', 
'Designers', 'Designer Exclusives', 'My Designers', 'Boutiques', 'Designer Boutique', 
'Workwear Boutique', 'Wedding Boutique', 'Basic Essentials', 'Clothing', 'Denim', 'Dresses', 
'Leather', 'Leggings', 'Lingerie', 'Maternity', 'Pants', 'Shorts', 'Skirts', 'Suit Separates', 
'Swimwear', 'Tops', 'Vests', 'Shoes', 'Shop All', 'Booties', 'Boots', 'Designer Boutique', 'Flats', 
'Pumps', 'Sandals', 'Sport', 'Bags', 'Shop All', 'Baby Bags', 'Backpacks', 'Beach Bags', 
'Black Handbags', 'Clutches', 'Cosmetic Pouches', 'Designer Boutique', 'Hobos', 'Satchels', 
'Shoulder Bags', 'Totes', 'Wallets', 'Weekend Bags', 'Accessories', 'Jewelry', 'Belts', 'Books', 
'Designer Boutique', 'Eyewear', 'Gloves', 'Hair Accessories', 'Hats', 'Hosiery', 'Keychains', 
'Product Care', 'Tech Accessories', 'Umbrellas', 'Watches', 'Winter Accessories', 'Sale', 
'Shop All', 'Clothing', 'Bags', 'Shoes', 'Accessories', 'Designer Boutique', 'Lookbooks', 
'Fashion Features', 'Latest Lookbook', 'My Shopbop', 'Account', 'Orders', 'My Designers', 
'My', 'My Reviews', 'shipping', 'zipcode', 'ground shipping']


def open_site(url):
	webpage = urlopen(url)
	soup = BeautifulSoup(webpage)
	webpage.close()
	return soup

def split_class(url, classes):
	soup = open_site(url)
	class_list = []
	classes = classes.split(',')
	for specific_class in classes:
		if specific_class:
			class_list.append(specific_class)
	return class_list

def first_time(url, classes):
	best_div = {}
	class_list = split_class(url, classes)
	title_list = []
	soup = open_site(url)
	for specific_class in class_list:
		product = soup.select(".%s" % (specific_class))
		title = get_titles(product, specific_class)
		if title:			
			best_div[specific_class]= title
	return best_div

def get_titles(product, specific_class):
	title_list = []
	title_matches = re.finditer(">\s*?(\w\w+\s*?\w*?)\s*?<", str(product))
	titles = [match_obj.group(1) for match_obj in title_matches]
	for title in titles:
		print title
		if wanted_title(title) and title not in title_list:
			title_list.append(title)
	return title_list

def wanted_title(title):
	for unwanted in unwanted_titles:
		if title.lower() == unwanted.lower():
			return False
	return True

def find_best_price_div(url, classes):
	similar_price = []
	price_divs = {}
	class_list = split_class(url, classes)
	soup = open_site(url)
	for specific_class in class_list:
		product = soup.select(".%s" % (specific_class))
		price_list = find_prices(product, specific_class)
		for price in price_list:
			if price and price not in similar_price:
				similar_price.append(price)
		price_divs[specific_class] = price_list
	return price_divs


def find_prices(product, specific_class):
	price_options = ["\$\d+.?\d*", "\d+.?\d*?\s?USD?"]
	price_list = []
	for price_type in price_options:
		prices = re.findall("%s" %(price_type), str(product))
		print prices
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
				img_id = image['id']
				i.save('./static/img/productImage' , 'jpeg')
				images[image['id']]= i 
	return images
