from urllib2 import urlopen
from bs4 import BeautifulSoup
import unittest
import re
#reg shopbop item
url1 = "http://www.shopbop.com/page-loafer-flat-31-phillip/vp/v=1/845524441951002.htm?folderID=2534374302165281&fm=other-shopbysize-viewall&colorId=12867"
#shopbop item on sale
url3 ="http://www.shopbop.com/revolution-joanna-bag-marc-by/vp/v=1/845524441945199.htm?folderID=2534374302076306&fm=sale-category-shopbysize-viewall&colorId=17384"

webpage = urlopen(url1)
soup = BeautifulSoup(webpage)



def choose_site(url):
	webpage = urlopen(url)
	soup = BeautifulSoup(webpage)
	product = soup.select("body #productInformation")
	return product

def choose_price(url):
	webpage = urlopen(url)
	soup = BeautifulSoup(webpage)
	product = soup.select("body #productInformation")
	price = re.search("\$\d+", str(product))
	return price.group()

# prices = soup.select("body priceTag")
# if prices:
# 	for price in prices:
# 		priceTag = re.search("\$\d+", str(price))
# 		print priceTag.group()	

# re.compile("")

# priceParent = [priceTag.parent for priceTag in soup.findAll(text=re.compile("\$\d+"))]
# for price in priceParent:
# 	print price


choose_site(url1)

class TestSequenceFunctions(unittest.TestCase):
	def test_price(self):
		self.assertEqual('$375', choose_price(url1))	
	def test_brand(self):
		self.assertEqual('')



if __name__ == '__main__':
    unittest.main()


# titleTag = soup.html.head.title
# print titleTag
# priceTag = re.search("price", str(soup.select("body")))
