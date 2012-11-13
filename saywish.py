from flask import Flask, render_template, redirect, request, g, session
from model import SESSION as db_session

import model
import scrapedoc

app = Flask(__name__)
SECRET_KEY = "SOMETHING"
app.config.from_object(__name__)

@app.route("/get_wishes/", methods = ["GET"])
def get_wishes():
	ids = request.args['items']
	website = request.args['weburl']
	beautiful = scrapedoc.first_time(website, ids)
	images = scrapedoc.find_images(website)
	return render_template("get_wish.html", beautiful = beautiful, images = images, website = website)


if __name__ == "__main__":
    app.run(debug = True)
