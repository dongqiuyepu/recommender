# about to scrape some restaurant data from google

import urllib2
import json
from time import sleep

google_api_url = "https://maps.googleapis.com/maps/api/place/search/json?"
google_api_key = "AIzaSyALqS94feM23XvecR32nmalhEHFg1nBMu4"


def get_restaurants(lat, log, radius=50000, pages=2):
    uri = "{0}key={1}&location={2},{3}&radius={4}&types=food"\
        .format(google_api_url, google_api_key, lat, log, radius)

    results_json = json.loads(urllib2.urlopen(uri).read())
    if results_json['status'] != "OK":
        raise Exception("Error using google place service.")

    next_page_token = results_json['next_page_token'] if 'next_page_token' in results_json else ''
    restaurants = results_json['results']

    # get remaining pages
    for i in xrange(1, pages):
        if not next_page_token:
            break
        sleep(2)
        uri_next_page = "{0}key={1}&pagetoken={2}"\
            .format(google_api_url, google_api_key, next_page_token)

        results_json = json.loads(urllib2.urlopen(uri_next_page).read())
        if results_json['status'] != "OK":
            raise Exception("Error using google place service.")

        next_page_token = results_json['next_page_token'] if 'next_page_token' in results_json else ''
        restaurants += results_json['results']

    return restaurants

if __name__ == '__main__':
   restaurants = get_restaurants(lat=37.7749295, log=-122.4194155)
   print len(restaurants)