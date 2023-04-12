from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField, SelectField, validators
import os
from wtforms.validators import NumberRange
import main_functions
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)


url = "http://acnhapi.com/v1a/backgroundmusic/"
response = requests.get(url).json()  # making the request
main_functions.save_to_file(response, "bgm.json")  # saving the response to a JSON file

#Choose Weather: Rainy, Snowy, Sunny
#Choose by Hour: 1-24

bgm_info = main_functions.read_from_file("bgm.json") # reading from the newly created JSON file
lst = [] # initializing an empty list
for i in ["hour"]:
    if i["hour"] == hour:
        lst.append(i["music_uri"])


class Music(FlaskForm):
     hour = IntegerField("Select an Hour",validators=[NumberRange(min=1, max=24, message='Invalid length')])
     weather = SelectField("Select the Weather", choices=[("Sunny"),
                                                          ("Rainy"),
                                                          ("Snowy")
                                                          ])
     submit = SubmitField('Submit')


@app.route('/', methods=['GET', 'POST'])
def index():
    form = Music()
    if form.validate_on_submit():
         hour_entered = form.hour.data
         weather_entered = form.weather.data
         list_of_bgm = get_list_of_bgm(hour_entered, weather_entered,url)
         return render_template("bgm_info.html",list_of_bgm=list_of_bgm,length=len(list_of_bgm),weather_entered=weather,hour_entered=hour)
    return render_template('ACNH.html', form=form)

if __name__ == '__main__':
    app.run()