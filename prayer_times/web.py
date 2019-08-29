import bottle
from bottle import route

from  prayer_times.lib import db, DiyanetApiV1

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
    return api.daily(nid=db.get(name))


@route('/api/<nid:int>/daily')
def api_daily_by_id(nid):
    return api.daily(nid)

app = bottle.default_app()

if __name__ == '__main__':
    # print(api.ulkeler())
    bottle.run(host='0.0.0.0', port=8000, debug=False, reloader=False)
