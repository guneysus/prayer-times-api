#!usr/bin/env python

import sys
from prayer_times.data import db, city_db, country_db
from pprint import pprint
import click
import requests
import json
import codecs
import os


def ensure_dir(file_path):
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)


def get_json(path, host):
    url = host + path
    r = requests.get(url)
    r.raise_for_status()
    return (r.json(), path)

def save_json(data, path, base_folder):
    file_path = base_folder + path # + '.json'
    ensure_dir(file_path)

    with codecs.open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f)

    return path

@click.command()
@click.option('--city', '-c', type=str, required=True)
@click.option('--period', '-p', type=str, required=True)
@click.option('--host', '-h', type=str, required=True)
@click.option('--basedir', '-b', type=str, required=True)
def main(city, period, host, basedir):

    helper = UrlHelper()
    url_list = helper.custom_cities(city.split(','), period.split(','))
    # full_urls = map(lambda x: (x, host + x), url_list)
    # dump_list(full_urls)
    results = map(lambda x: get_json(x, host), url_list)
    file_results = map(lambda x: save_json( *x, basedir), results)
    return list(file_results)

class UrlHelper:
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
