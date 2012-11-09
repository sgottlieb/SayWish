from flask import Flask, render_template, redirect, request, g, session
from model import SESSION as db_session

import model
import scrapedoc

app = Flask(__name__)
SECRET_KEY = "SOMETHING"
app.config.from_object(__name__)

@app.route("/get_wishes/", methods = ["GET"])
def get_wishes():
	print "getting ids"
	ids = request.args['items']
	website = request.args['weburl']
	print "going to scrapedoc"
	beautiful = scrapedoc.choose_price(website, ids)
	return render_template("get_wish.html", beautiful=beautiful)


if __name__ == "__main__":
    app.run(debug = True)
