from model import SESSION, Item, Website, Wishlist,Base
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import model
import datetime
import scrapedoc
import os
import smtplib

def checker():
	f = open("somefile.txt", "w")
	for item in SESSION.query(Item).order_by(Item.id):
		price_list =[]
		website = SESSION.query(Website).filter_by(hostname=item.host_url).first()
		prices = scrapedoc.price_check(item.url, website.price_class)
		for price in prices:
			this_price = price.split('$')
			item_price = item.price.split('$')
			if float(this_price[1]) < float(item_price[1]):
				item.price = price
				user_emails = get_users(item.id)
				for users in user_emails:
					email_price(users, price, item.url)
				price_list.append(price)
		f.write(str(price_list))

	f.close()
	SESSION.commit()

def get_users(input_item_id):
	user_emails = []
	wishlists = SESSION.query(Wishlist).filter_by(item_id=input_item_id).all()
	for wishlist in wishlists:
		user_emails.append(wishlist.user.email)
		print wishlist.user.email
	return user_emails

def email_price(user_email, price, item_url):
	print "email"
	msg = MIMEMultipart('alternative')
	msg['Subject'] = "Say Wish! Your item's on Sale"
	msg['From']    = "SayWish <gottlieb0@gmail.com>" # Your from name and email address
	msg['To']      = "%s" % (user_email)
	text = "Your Item is on sale! "
	html = "<a href='%s'>Here!</a>" %(item_url)
	part2 = MIMEText(html, 'html')
	part1 = MIMEText(text, 'plain')
	username = 'gottlieb0@gmail.com'
	password = '642b47a4-67f4-4594-bd48-80308e2bbc59'
	msg.attach(part1)
	msg.attach(part2)
	s = smtplib.SMTP('smtp.mandrillapp.com', 587)
	s.login(username, password)
	s.sendmail(msg['From'], msg['To'], msg.as_string())
	s.quit()

checker()
