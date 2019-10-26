#!usr/bin/env python

import sys
from prayer_times.data import db, city_db, country_db
from pprint import pprint
import click
import requests


def get_json(url):
    r = requests.get(url)
    r.raise_for_status()
    return r.json()

@click.command()
@click.option('--city', '-c', type=str, required=True)
@click.option('--period', '-p', type=str, required=True)
@click.option('--host', '-h', type=str, required=True)
def main(city, period, host):

    urls = Urls()
    url_list = urls.custom_cities(city.split(','), period.split(','))
    full_urls = map(lambda x: host + x, url_list)
    # dump_list(full_urls)
    results = tuple(map(lambda x: get_json(x), full_urls))
    print(results)

class Urls:
    @property
    def all(self):
        result = []
        result.extend(self.countries())
        result.extend(self.cities_all())
        result.extend(self.counties_all())
        result.extend(self.cities_by_name(periods=self.periods()))

        return result
    
    def countries(self):
        return [ '/api/countries/']

    def cities_all(self):
        return [f'/api/countries/{country_db[k]}/cities' for k in country_db]

    def counties_all(self):
        return [f'/api/countries/{country_id}/cities/{city_db[city_name]}/counties/{db[county_name]}/{period}' for city_name in city_db for county_name in db for period in self.periods for country_id in country_db.values()]
    
    def periods(self):
        return ['daily', 'weekly', 'monthly', 'ramadan-timetable', 'sacrifice', 'ramadan', 'ramadan-all', 'sacrifice-all']

    def cities_by_name(self, periods=['daily']):
        return [f'/api/{name}/{period}' for name in city_db for period in periods]

    def custom_cities(self, cities, periods):
        return [f'/api/{name}/{period}' for name in cities for period in periods]

def dump_list(urls):
    print(*urls, sep='\n', file=sys.stdout)

if __name__ == "__main__":
    main()
