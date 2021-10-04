 # "THE BEER-WARE LICENSE" (Revision 42):
 # <vkrmk13@gmail.com> wrote this file.  As long as you retain this notice you
 # can do whatever you want with this stuff. If we meet some day, and you think
 # this stuff is worth it, you can buy me a beer in return. Vitaliy Kreminskii

from bs4 import BeautifulSoup
from utils.prettifiers import drop_entities
import requests

ternopil_station_id = '610100'

def get_stations():
  url = 'http://bus.com.ua/cgi-bin/tablo.pl'
    
  response = requests.get(url)
  html = response.text
  soup = BeautifulSoup(html, 'html.parser')

  table = soup.find_all('table')[1]
  table_rows = table.find_all('tr')

  stations = []

  for row in table_rows:
    rows = row.find_all('td')
    for cell in rows:
      link_node = cell.find('a')

      if not link_node:
        continue

      station_id = link_node['href'].split('=')[1]

      station = {
        'id': station_id,
        'name': link_node.text,
        'connection_quality': cell.find('img')['alt'].lstrip()
      }

      stations.append(station)

  return stations[1:]

# Returns all the timetable routes for the specific station
def get_routes_by_station_id(station_id = ternopil_station_id):
  url = 'http://bus.com.ua/cgi-bin/tablo.pl?as=' + station_id

  response = requests.get(url)

  html = response.text

  soup = BeautifulSoup(html, 'html.parser')

  table = soup.find_all('table')[1].find_all('table')[1]
  table_rows = table.find_all('tr')[2:]

  routes = []

  for row in table_rows:
    cells = row.find_all('td')

    if (not hasattr(cells[0].find('font'), 'text')):
      continue

    route_cell_inner_text = drop_entities(cells[1].text)
    arrival_station = drop_entities(cells[1].find_all('font')[0].text)
    departure_station = drop_entities(route_cell_inner_text[:-len(arrival_station) - 3])
    bus_model_link = cells[4].find('a')

    route = {
      'date': cells[0].find('font').text,
      'departure_time': cells[0].find('b').text,
      'arrival_time': cells[2].text,
      'departure_station': departure_station,
      'arrival_station': arrival_station,
      'ticket_price': drop_entities(cells[3].text),
      'bus_model': bus_model_link.text if hasattr(bus_model_link, 'text') else None,
      'status': cells[5].text,
      'seats_available': drop_entities(cells[6].text)
    }

    routes.append(route)

  return routes