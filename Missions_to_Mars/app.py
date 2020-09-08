from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/Mars"
mongo = PyMongo(app)

@app.route("/")
def index():
    results = mongo.db.results.find_one()
    return render_template("index.html", results=results)

@app.route("/scrape")
def scraper():
    results = mongo.db.results
    mars_data = scrape_mars.scrape()
    results.update({}, mars_data, upsert=True)
    return redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)

