# about to scrape some restaurant data from google

import urllib2
import json
from time import sleep

google_place_batch_api = "https://maps.googleapis.com/maps/api/place/search/json?"
google_place_detail_api = "https://maps.googleapis.com/maps/api/place/details/json?placeid=&key="
google_api_key = "AIzaSyALqS94feM23XvecR32nmalhEHFg1nBMu4"


def get_restaurants(lat, log, radius=5000, pages=4):
    uri = "{0}key={1}&location={2},{3}&radius={4}&types=food" \
        .format(google_place_batch_api, google_api_key, lat, log, radius)

    results_json = json.loads(urllib2.urlopen(uri).read())
    if results_json['status'] != "OK":
        raise Exception("Error using google place service.")

    next_page_token = results_json['next_page_token'] if 'next_page_token' in results_json else ''
    restaurants = results_json['results']

    fo = open("restaurants_outline.txt", "w+")
    fo.write(json.dumps(restaurants) + "\n")
    # get remaining pages
    for i in xrange(1, pages):
        if not next_page_token:
            break
        sleep(2)
        uri_next_page = "{0}key={1}&pagetoken={2}" \
            .format(google_place_batch_api, google_api_key, next_page_token)

        results_json = json.loads(urllib2.urlopen(uri_next_page).read())
        if results_json['status'] != "OK":
            raise Exception("Error using google place service.")

        next_page_token = results_json['next_page_token'] if 'next_page_token' in results_json else ''

        fo.write(json.dumps(results_json['results']) + "\n")
        # restaurants += results_json['results']

    fo.close()
    # return restaurants


if __name__ == '__main__':
    restaurants_list = get_restaurants(lat=37.7749295, log=-122.4194155)
    # assert isinstance(restaurants_list, list)
