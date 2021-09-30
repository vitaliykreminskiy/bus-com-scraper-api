from bs4 import BeautifulSoup
import requests

ternopil_station_id = '610100'

def get_stations():
  url = 'http://bus.com.ua/cgi-bin/tablo.pl'
    
  response = requests.get(url)
  html = response.text
  soup = BeautifulSoup(html, 'html.parser')

  #to be continued



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

    route_cell_inner_text = cells[1].text.replace(u'\xa0', '')
    arrival_station = cells[1].find_all('font')[0].text.replace(u'\xa0', '')
    departure_station = route_cell_inner_text[:-len(arrival_station) - 3].replace(u'\xa0', '')
    bus_model_link = cells[4].find('a')

    route = {
      'date': cells[0].find('font').text,
      'departure_time': cells[0].find('b').text,
      'arrival_time': cells[2].text,
      'departure_station': departure_station,
      'arrival_station': arrival_station,
      'ticket_price': cells[3].text.replace(u'\xa0', ''),
      'bus_model': bus_model_link.text if hasattr(bus_model_link, 'text') else None,
      'status': cells[5].text,
      'seats_available': cells[6].text.replace(u'\xa0', '')
    }

    routes.append(route)

  return routes
