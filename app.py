import json
import os

import requests
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField
from wtforms.validators import NumberRange

import main_functions

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Choose Weather: Rainy, Snowy, Sunny
# Choose by Hour: 1-24


class Music(FlaskForm):
    hour = IntegerField("Select an Hour", validators=[NumberRange(min=0, max=24, message='Invalid length')])
    weather = SelectField("Select the Weather", choices=["Sunny",
                                                         "Rainy",
                                                         "Snowy"
                                                         ])
    submit = SubmitField('Submit')


def request_music():
    url = "http://acnhapi.com/v1a/backgroundmusic/"
    response = requests.get(url).json()  # making the request
    main_functions.save_to_file(response, "bgm.json")  # saving the response to a JSON file
    return response

bgm_info = main_functions.read_from_file("bgm.json")  # reading from the newly created JSON file


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Music()
    if request.method == "POST":
        hour_entered = int(request.form['hour'])
        weather_entered = request.form['weather']

        with open('bgm.json', 'r') as f:
            bgm_music = json.load(f)

        bgm_music = request_music()
        music_list = []
        for i in bgm_music:
            if i["hour"] == hour_entered and i["weather"] == weather_entered:
                music_list.append((i["file-name"], i["music_uri"], i["hour"],i["weather"]))
                print(f"Match found: {i}")
            # music_list.append((i["file-name"], i["music_uri"]))


        return render_template("bgm_info.html", music_list=music_list, hour_entered=hour_entered,
                               weather_entered=weather_entered)
    return render_template('ACNH.html', form=form)


if __name__ == '__main__':
    app.run()
