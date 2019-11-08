from flask import Flask, render_template, request
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map
from geopy.geocoders import Nominatim

import pandas as pd
import pickle
import json

# Import data
df = pd.read_csv("all_map_points.csv")

# Import disaster classification model
model = pickle.load(open('./relevant_tweet_model.p', 'rb'))

# Make predictions
df['preds'] = model.predict(df['text'])

# Select disaster related tweets to map
df = df.loc[df['preds']==1,:].reset_index(drop=True)

# Make dictionary to map disaster related tweets using GoogleMaps
lats = df.loc[:, 'lat']
longs = df.loc[:,'long']
texts = df.loc[:,'text']

marker_list = []
for i in range(df.shape[0]):
    spot_dict = {'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
                 'lat': lats[i],
                 'lng': longs[i],
                 'infobox': "<b>" + texts[i] +"<br>"
                }
    marker_list.append(spot_dict)


app = Flask("Test App", template_folder = "./templates")

# Sign into GoogleMaps using API key in "map_key.json" in the format of "{'api_key': type your API key}"
map_creds = open("./map_key.json", "r")
creds = json.loads(map_creds.read())
app.config['GOOGLEMAPS_KEY'] = creds["api_key"]

# Initialize the extension
GoogleMaps(app)

@app.route('/') # this is what happens when the user visits the website

# create the controller
def home():
    # return the view
    return render_template('form.html')

@app.route("/view_map")
def mapview():
    user_input = request.args

    geolocator = Nominatim()
    location = geolocator.geocode(user_input['address'])
    out_lat = location.latitude
    out_lng = location.longitude

    sndmap = Map(
        identifier="sndmap",
        lat= out_lat,
        lng= out_lng,
        markers= marker_list,
        style = "height:500px;width:90%;margin:0;align:center;"
    )
    return render_template('example.html', sndmap=sndmap)

# run the app
if __name__ == '__main__':
	app.run(debug=True)
