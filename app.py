from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
from Scrape_mars import scrape

app = Flask(__name__)

# setup mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/app")



@app.route('/')
def index():                
    # write a statement that finds all the items in the db and sets it to a variable
    mars_data = mongo.db.mars.find_one()

    # render an index.html template and pass it the data you retrieved from the database
    return render_template("index.html", mars_data=mars_data)

@app.route("/scrape")
def scraper():
    
    mars = mongo.db.mars
    mars_data = scrape()
    mars.update({}, mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
