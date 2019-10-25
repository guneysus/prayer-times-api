#!usr/bin/env python
from prayer_times.data import db, city_db, country_db
from pprint import pprint as print

def urls():
    result = []
    periods = ['daily', 'weekly', 'monthly', 'ramadan-timetable', 'sacrifice', 'ramadan', 'ramadan-all', 'sacrifice-all'][:]

    result.extend([f'/api/{name}/{period}' for name in city_db for period in periods])

    return result
    
    result.extend([ '/api/countries/'])

    for country_id in country_db.values():
        result.extend([f'/api/countries/{country_db[k]}/cities' for k in country_db])

    result.extend([f'/api/countries/{country_id}/cities/{city_db[city_name]}/counties' for city_name in city_db])

    result.extend([f'/api/countries/{country_id}/cities/{city_db[city_name]}/counties/{db[county_name]}' for city_name in city_db for county_name in db])

    result.extend([f'/api/countries/{country_id}/cities/{city_db[city_name]}/counties/{db[county_name]}/{period}' for city_name in city_db for county_name in db for period in periods])


        # for name, county_id in db.items():
        #     result.extend([f'/api/countries/{country_id}/cities/{city_id}/counties' for k in city_db])

    return result

def main():
    print(urls())

if __name__ == "__main__":
    main()