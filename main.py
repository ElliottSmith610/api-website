import requests as rq
from flask import Flask, render_template, request
import pycountry

age_api = "https://api.agify.io"
gender_api = "https://api.genderize.io"
nationality_api = "https://api.nationalize.io"


def predict(name):
    param = {
        "name": name,
        }

    age = rq.get(age_api, params=param).json()["age"]
    gender = rq.get(gender_api, params=param).json()["gender"]
    nation = rq.get(nationality_api, params=param).json()["country"][0]["country_id"]
    country_name = pycountry.countries.get(alpha_2=nation).name
    return {
        "name": name,
        "age": age,
        "gender": gender.title(),
        "nationality": country_name,
        }


app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def home():
    data = None
    if request.method == "POST":
        data = predict(request.form.get("name"))

    return render_template("index.html", data=data)


if __name__ == "__main__":
    app.run(debug=True)
