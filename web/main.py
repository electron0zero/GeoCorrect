import os
import sqlite3
import logging
from flask import Flask, render_template, url_for, g, abort
from flask_script import Manager
from flask_bootstrap import Bootstrap
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map, icons
import requests

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'data.sqlite'),
    DEBUG=False,
    SECRET_KEY='development key',
    GOOGLEMAPS_KEY='AIzaSyAZzeHhs-8JZ7i18MjFuM35dJHq70n3Hx4',
    FSQ_CLIENT_ID="KWN5LLYHWCOD21MDIUEGN5FUONQLYRYSI4ESBC2GB5JCDITC",
    FSQ_CLIENT_SECRET="TM2KT2FNC2P00MVH4BRWB32FXLJPOFDFRTL0KHHHWT3MSV0C"
))

manager = Manager(app)
bootstrap = Bootstrap(app)
GoogleMaps(app)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    db = get_db()
    query = "SELECT venues.venue_id, venues.lat, venues.lng, results.lat as lat_new, results.lng as lng_new  FROM venues LEFT JOIN results ON venues.venue_id = results.venue_id LIMIT 1000"
    cur = db.execute(query)
    entries = cur.fetchall()
    # app.logger.info(entries)
    return render_template('index.html', entries=entries)


@app.route('/<venue_id>')
def show_map(venue_id):
    map_data = get_map_obj(venue_id)
    return render_template('show_map.html', map_obj=map_data, venue_id=venue_id)


@app.route('/table/<venue_id>')
def show_map_table(venue_id):
    # fetch data from db
    checkins, old_location, new_location = fetch_data(venue_id)
    venue_info_data = get_location_info(venue_id)
    return render_template('show_map_table.html', checkins=checkins, old_loc=old_location, new_loc=new_location, venue_id=venue_id, venue_info=venue_info_data)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500


def get_map_obj(venue_id):
    # fetch data from db
    checkins, old_location, new_location = fetch_data(venue_id)

    # Build Map object for Showing
    markers_list = []
    new_lat = ""
    new_lng = ""
    old_lat = ""
    new_lng = ""
    # Add checkins in Markers list
    for lat, lng in checkins:
        dict = {}
        dict['icon'] = url_for('static', filename='yc.png')
        dict['lat'] = lat
        dict['lng'] = lng
        dict['infobox'] = "Checkin"
        markers_list.append(dict)

    # Add old Location in Markers list
    for lat, lng in old_location:
        dict = {}
        dict['icon'] = url_for('static', filename='bo.png')
        dict['lat'] = lat
        dict['lng'] = lng
        dict['infobox'] = "Old Location"
        markers_list.append(dict)
        old_lat = lat
        old_lng = lng

    # Add New Location in Markers list
    for lat, lng in new_location:
        dict = {}
        dict['icon'] = url_for('static', filename='gn.png')
        dict['lat'] = lat
        dict['lng'] = lng
        dict['infobox'] = "New Location"
        markers_list.append(dict)
        new_lat = lat
        new_lng = lng

    # Build a polyline between new and old location
    # build plyline infobox
    venue_info_data = get_location_info(venue_id)
    venue_url = "<a target=\"_blank\" href=\"" + venue_info_data['venue_canonicalUrl'] + "\">" + venue_info_data['venue_canonicalUrl'] + "</a>"

    infobox_str = "<h5 class=\"text-center\">Venue Information</h5>" + venue_info_data['venue_name'] + "<br>" + venue_info_data['venue_formattedAddress'] + "<br>" + venue_url

    polyline = {}
    polyline['stroke_color'] = '#448aff'
    polyline['stroke_opacity'] = '1.0'
    polyline['stroke_weight'] = '8'
    polyline['infobox'] = infobox_str
    path_list = []
    path_list.append((old_lat, old_lng))
    path_list.append((new_lat, new_lng))
    polyline['path'] = path_list

    fullmap = Map(
        identifier="fullmap",
        varname="fullmap",
        style=(
            "height:100%;"
            "width:100%;"
            "top:0;"
            "left:0;"
            "position:absolute;"
            "z-index:-1;"
        ),
        lat=new_lat,
        lng=new_lng,
        markers=markers_list,
        maptype="TERRAIN",
        polylines=[polyline],
        cluster=False,
        cluster_imagepath=url_for('static', filename='m2.png'),
        zoom="20"
    )
    return fullmap


def fetch_data(venue_id):
    db = get_db()
    query_checkins = "SELECT lat, lng FROM checkins WHERE venue_id = " + "'" + venue_id + "'"
    cur_checkins = db.execute(query_checkins)
    checkins = cur_checkins.fetchall()
    query_old_loc = "SELECT lat, lng FROM venues WHERE venue_id = " + "'" + venue_id + "'"
    cur_old_loc = db.execute(query_old_loc)
    old_location = cur_old_loc.fetchall()
    query_new_loc = "SELECT lat, lng FROM results WHERE venue_id = " + "'" + venue_id + "'"
    cur_new_loc = db.execute(query_new_loc)
    new_location = cur_new_loc.fetchall()

    if (len(checkins) is 0) or (len(old_location) is 0) or (len(new_location) is 0):
        app.logger.error("No data raise 404")
        abort(404)

    return checkins, old_location, new_location


def get_location_info(venue_id):
    # auth info
    c_id = app.config['FSQ_CLIENT_ID']
    c_sec = app.config['FSQ_CLIENT_SECRET']
    v = "20170101"
    # auth payload for request
    payload = {'client_id': c_id, 'client_secret': c_sec, 'v': v}

    base_url = "https://api.foursquare.com/v2/venues/"

    # request with venue_id and auth payload
    r = requests.get(base_url + venue_id, params=payload)
    # get these data fields and return
    # data fields = name, location(formattedAddress), canonicalUrl
    venue_name = "Not Found"
    venue_formattedAddress = "Not Found"
    venue_canonicalUrl = "Not Found"
    # get data we get 200 response code otherwise 'Not Found'
    if (r.status_code == 200):
            resp = r.json()
            venue_name = resp['response']['venue']['name']
            venue_formattedAddress = resp['response']['venue']['location']['formattedAddress']
            venue_canonicalUrl = resp['response']['venue']['canonicalUrl']

    # build venue info data dict
    venue_info_data = {}
    venue_info_data['venue_name'] = venue_name
    venue_info_data['venue_formattedAddress'] = ", ".join(venue_formattedAddress)
    venue_info_data['venue_canonicalUrl'] = venue_canonicalUrl

    return venue_info_data

if __name__ == '__main__':
    manager.run()
