from urllib2 import urlopen
from bs4 import BeautifulSoup
import re

weburl = "http://www.revolveclothing.com/DisplayProduct.jsp?product=MOTH-WJ147&c=&s=C&d=5&sc=Flare"
wids = "detail_cart1_price,priceLabel1,detail_cart1_price"

def choose_price(url, ids):
	webpage = urlopen(url)
	prices = []
	soup = BeautifulSoup(webpage)
	ids = ids.split(',')
	product = soup.select("body")

	prices.append(re.search("\$\d+", str(product)).group())
	print prices


choose_price(weburl, wids)