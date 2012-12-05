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
		return redirect("/main_wishes")
	return render_template("main.html")

@app.route('/authenticate', methods = ["POST"])
def login():
	email = request.form['email']
	password = request.form['password']
	user_id = model.User.authenticate(email, password)
	session['user_id'] = user_id
	g.user_id = session.get('user_id')
	if user_id != None:
		return redirect("/main_wishes")
	return "wrong password or email"

@app.route('/new_user', methods = ["POST"])
def newuser():
	email = request.form['email']
	password = request.form['password']
	user_id = model.User.new(email, password)
	session['user_id'] = user_id
	g.user_id = session['user_id'] 
	return redirect("/main_wishes")

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
		price_class, brand_class = [host_data.price_class], host_data.brand_class
	else:
		brand_class = scrapedoc.split_class(request.args['items'])
		price_class = brand_class
	groups = model.Wishlist.search_groups(user_id.id)
	brand = scrapedoc.first_time(website, brand_class)
	images = scrapedoc.find_images(website)
	prices = scrapedoc.find_best_price_div(website, price_class)
	host = scrapedoc.get_host(website)
	image_src = scrapedoc.find_images(website)
	return render_template("get_wish.html", brand = brand, images = images, website = website, prices = prices, host=host, image_src = image_src, groups=groups)

@app.route("/add_item", methods = ["POST"])
def newitem():
	# getting back (div class, specific)
	user_id = g.user_id
	website = request.form['specific_url']
	brand = request.form['brandname']
	other_brand = request.form['brandname_other']
	price = request.form['price']
	other_price = request.form['price_other']
	host = request.form['host']
	image_src = request.form['image_src']
	item_group = request.form['item_group']
	if item_group =="None, other":
		item_group = request.form['item_group_other']
	if brand != "None, other" and price != "None, other":
		price_info, brand_info = eval(price), eval(brand)
	elif brand == "None, other" and price == "None, other":
		price_info, brand_info = (None, other_price), (None, other_brand)
	elif brand == "None, other":
		price_info, brand_info = eval(price), (None, other_brand)
	elif price == "None, other":
		price_info, brand_info = (None, other_price), eval(brand)
	if scrapedoc.check_host(website) == None:
		model.Website.new(host, str(price_info[0]), str(brand_info[0]), None)
	item=model.Item.new(str(brand_info[1]), item_group, str(price_info[1]), website, host, image_src)
	model.Wishlist.new(user_id.id, item)
	return redirect("/main_wishes")

@app.route('/grouped_items/, methods=["GET"]')
def group_items():
	group_name = request.args['group']
	other_items = model.Wishlist.search(g.user_id.id)
	desired_group =[]
	for items in other_items:
		if items.item.title == group_name:
			desired_group.append(items.item)
	return render_template("wishlist.html", items= desired_group)

@app.route('/main_wishes')
def items():
	items = model.Wishlist.search(g.user_id.id)
	group_items = model.Wishlist.search_groups(g.user_id.id)
	best_groups ={}
	if items:
		for group in group_items:
			best_item =[1000000000, None]
			for item in items:
				if item.item.title == group:
					item_price = item.item.price.split('$')
					if best_item[0]>float(item_price[1]):
						best_item[0], best_item[1] =float(item_price[1]), item.item
			best_groups[group] = best_item[1]
	else:
		item_dict = None
	return render_template("main_wishlist.html", item_dict = best_groups)


@app.route('/wishlist/', methods=["GET"])
def delete_item():
	item_id = request.args['itemid']
	model.Item.delete(item_id)
	return redirect("/main_wishes")

if __name__ == "__main__":
	app.run(debug = True)
