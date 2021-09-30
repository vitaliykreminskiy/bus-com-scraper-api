from scraper import get_routes_by_station_id
from flask import Flask, jsonify, request

__app__ = 'Scraper API'

app = Flask(__app__)
ternopil_station_id = '610100'

@app.route('/timetable')
def show_timetable():
  request_station_id = request.args.get('station_id')
  station_id = request_station_id if request_station_id != None else ternopil_station_id

  return jsonify(get_routes_by_station_id(station_id))
