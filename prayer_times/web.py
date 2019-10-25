import bottle
from bottle import route

from .lib import db, DiyanetApiV1
import logging

logging.basicConfig(level=logging.INFO)

logging.debug('This is a debug message')
logging.info('This is an info message')
logging.warning('This is a warning message')
logging.error('This is an error message')
logging.critical('This is a critical message')

api = DiyanetApiV1()


@route('/api/countries/<country_id:int>/cities/<city_id:int>/counties/<county_id:int>/monthly')
def api_ulke_sehir_ilce_aylik(country_id, city_id, county_id):
    return api.monthly(county_id)


@route('/api/countries/<country_id:int>/cities/<city_id:int>/counties/<county_id:int>/weekly')
def api_ulke_sehir_ilce_haftalik(country_id, city_id, county_id):
    return api.weekly(county_id)


@route('/api/countries/<country_id:int>/cities/<city_id:int>/counties/<county_id:int>/daily')
def api_ulke_sehir_ilce_gunluk(country_id, city_id, county_id):
    return api.daily(county_id)


@route('/api/countries/<country_id:int>/cities/<city_id:int>/counties/<county_id:int>')
def api_ulke_sehir_ilce_detay(country_id, city_id, county_id):
    return api.county_detail(county_id)


@route('/api/countries/<country_id:int>/cities/<city_id:int>/counties')
def api_ulke_sehir_ilceler(country_id, city_id):
    return api.counties(city_id)


@route('/api/countries/<nid:int>/cities')
def api_ulke_sehirler(nid):
    return api.cities(nid)


@route('/api/countries')
def api_ulkeler():
    return api.countries()


@route('/api/<name:re:[a-z]+>/daily')
def api_daily_by_name(name):
    nid = db.get(name)
    logging.info(f'name: {name}, nid: {nid}')
    response = api.daily(nid)
    return response

@route('/api/<name:re:[a-z]+>/weekly')
def api_weekly_by_name(name):
    nid = db.get(name)
    logging.info(f'name: {name}, nid: {nid}')
    response = api.weekly(nid)
    return response

@route('/api/<name:re:[a-z]+>/monthly')
def api_monthly_by_name(name):
    nid = db.get(name)
    logging.info(f'name: {name}, nid: {nid}')
    response = api.monthly(nid)
    return response


@route('/api/<nid:int>/daily')
def api_daily_by_id(nid):
    return api.daily(nid)

@route('/api/<nid:int>')
def api_bayram(nid):
    return api.daily(nid)

app = bottle.default_app()

if __name__ == '__main__':
    # print(api.ulkeler())
    bottle.run(host='0.0.0.0', port=8000, debug=False, reloader=False)
