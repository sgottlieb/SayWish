from flask import Flask, render_template, redirect, request, g, session
from model import SESSION as db_session

import model
import scrapedoc

app = Flask(__name__)
SECRET_KEY = "SOMETHING"
app.config.from_object(__name__)

@app.before_request
def load_user_id():
	g.user_id = session.get('user_id')

@app.teardown_request
def unload(exception = None):
	db_session.remove()

@app.route("/")
def index():
	if g.user_id:
		return render_template("wishlist.html")
	return render_template("main.html")

@app.route('/authenticate', methods = ["POST"])
def login():
	email = request.form['email']
	password = request.form['password']
	user_id = model.User.authenticate(email, password)
	session['user_id'] = user_id
	g.user_id = session.get('user_id')
	if user_id != None:
		return render_template("wishlist.html", user_id=user_id)
	return "wrong password or email"

@app.route('/new_user', methods = ["POST"])
def newuser():
	email = request.form['email']
	password = request.form['password']
	user_id = model.User.new(email, password)
	return render_template("wishlist.html", user_id=user_id)

@app.route('/logout')
def logout():
	session.pop('user_id', None)
	return render_template("main.html")

@app.route("/get_wishes/", methods = ["GET"])
def get_wishes():
	user_id = g.user_id
	website = request.args['weburl']
	host_data = scrapedoc.check_host(website)
	if host_data:
		price_class, brand_class = [host_data.price_class], [host_data.brand_class]
	else:
		brand_class = scrapedoc.split_class(request.args['items'])
		price_class = brand_class
	brand = scrapedoc.first_time(website, brand_class)
	images = scrapedoc.find_images(website)
	prices = scrapedoc.find_best_price_div(website, price_class)
	host = scrapedoc.get_host(website)
	return render_template("get_wish.html", brand = brand, images = images, website = website, prices = prices, host=host)

@app.route("/add_item", methods = ["POST"])
def newitem():
	# getting back (div class, specific)
	user_id = g.user_id
	website = request.form['specific_url']
	brand = request.form['brandname']
	price = request.form['price']
	host = request.form['host']
	item_group = request.form['item_group']
	price_info, brand_info = eval(price), eval(brand)
	if scrapedoc.check_host(website) == None:
		model.Website.new(host, str(price_info[0]), str(brand_info[0]), None)
	item = model.Item.new(str(brand_info[1]), item_group, str(price_info[1]), website, host, None)
	model.Wishlist.new(user_id.id, item)
	items = model.Wishlist.search(user_id.id)
	item_objects =[]
	for item in items:
		item_objects.append(model.Item.search(item.item_id))
	return render_template("wishlist.html", user_id = user_id, items = item_objects)

if __name__ == "__main__":
	app.run(debug = True)
