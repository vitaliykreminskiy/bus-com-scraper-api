from scraper import get_routes_by_station_id
from flask import Flask, jsonify

__app__ = 'Scraper API'

app = Flask(__app__)

@app.route('/timetable')
def show_timetable():
  return jsonify(get_routes_by_station_id())
