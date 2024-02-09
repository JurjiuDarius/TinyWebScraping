from flask import Flask, render_template
from apartment_service import fetch_apartments

app = Flask(__name__)


@app.route("/")
def hello():
    apartments = fetch_apartments()
    return render_template("apartments.html", apartments=apartments)


app.run(host="0.0.0.0", port=8080)
