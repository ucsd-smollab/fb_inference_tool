from flask import Flask
from flask import request
from flask import render_template

app = Flask(__name__)

@app.route("/go", methods=("GET", "POST"))
def go():
    """Display results."""
    predictions = request.args
    friends = predictions["friends"]
    inferences = predictions["inferences"]
    return render_template("index.html", predictions=predictions, friends=friends, inferences=inferences)
