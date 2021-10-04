 # "THE BEER-WARE LICENSE" (Revision 42):
 # <vkrmk13@gmail.com> wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. Vitaliy Kreminskii

from scraper import get_routes_by_station_id, get_stations
from flask import Flask, jsonify, request

__app__ = 'Scraper API'

app = Flask(__app__)
ternopil_station_id = '610100'

@app.route('/timetable')
def show_timetable():
  request_station_id = request.args.get('station_id')
  station_id = request_station_id if request_station_id != None else ternopil_station_id

  return jsonify(get_routes_by_station_id(station_id))

@app.route('/stations')
def show_stations():
  return jsonify((get_stations()))
