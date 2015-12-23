# about to scrape some restaurant data from google

import json
import logging
import urllib2
import os
from json import JSONEncoder
from time import sleep

from elasticsearch import Elasticsearch

root_path = "../../../"

google_place_batch_api = "https://maps.googleapis.com/maps/api/place/search/json?"
google_place_detail_api = "https://maps.googleapis.com/maps/api/place/details/json?"
google_api_key = "AIzaSyALqS94feM23XvecR32nmalhEHFg1nBMu4"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_restaurants(lat, log, fname, radius=1000, pages=10):
    uri = "{0}key={1}&location={2},{3}&radius={4}&types=food" \
        .format(google_place_batch_api, google_api_key, lat, log, radius)

    results_json = json.loads(urllib2.urlopen(uri).read())
    if results_json['status'] != "OK":
        logger.info("Error using google place service.")

    next_page_token = results_json['next_page_token'] if 'next_page_token' in results_json else ''
    restaurants = results_json['results']

    fo = open(fname, "w+")
    fo.write(json.dumps(restaurants) + "\n")

    # get remaining pages
    for i in xrange(1, pages):
        if not next_page_token:
            break
        sleep(3)
        uri_next_page = "{0}key={1}&pagetoken={2}" \
            .format(google_place_batch_api, google_api_key, next_page_token)

        results_json = json.loads(urllib2.urlopen(uri_next_page).read())
        if results_json['status'] != "OK":
            logger.info("Error using google place service.")
            break

        next_page_token = results_json['next_page_token'] if 'next_page_token' in results_json else ''

        fo.write(json.dumps(results_json['results']) + "\n")

    fo.close()


def get_all_restaurants_in_sf():
    lat_l = 37.636529
    lat_r = 37.806258
    log_l = -122.513008
    log_r = -122.360573

    logger.info("Start grid search for lat and log.")
    for lat_step in xrange(0, 18):
        for log_step in xrange(0, 16):
            lat = lat_l + lat_step * 0.01
            log = log_l + log_step * 0.01
            fname = "{0}data/restaurants_sf_{1}_{2}".format(root_path, lat, log)
            logger.info("Searching for lat: {0} and log: {1}".format(lat, log))
            get_restaurants(lat, log, fname)


def process_all_restaurant_file():
    restaurants_list = []
    for file_name in os.listdir(root_path + "data"):
        logger.info("Processing file: " + file_name)
        for line in open(root_path + "data/" + file_name):
            line_json = json.loads(line)
            restaurants_list = restaurants_list + line_json if len(line_json) > 0 else restaurants_list

    logger.info("Total number of restaurants: {0}".format(len(restaurants_list)))

    # save all restaurants to file
    fo = open(root_path + "all_restaurants_sf", "w+")
    for res in restaurants_list:
        fo.write(json.dumps(res))
        fo.write("\n")
    fo.close


def get_all_restaurants_details():
    outfname = "all_restaurants_details_sf"
    fo = open(root_path + outfname, "w+")
    for line in open(root_path + "all_restaurants_sf_r1000", "r+"):
        # get place id
        place_id = json.loads(line)['place_id']

        logger.info("Getting restaurant detail for: " + place_id)

        # request restaurant detail
        uri = "{0}placeid={1}&key={2}".format(google_place_detail_api, place_id, google_api_key)
        results_json = json.loads(urllib2.urlopen(uri).read())
        if results_json['status'] != 'OK':
            logger.info("Error: can't make request for " + uri)
            continue

        fo.write(json.dumps(results_json['result']))
        fo.write('\n')

    fo.close()


def index_restaurants_to_es():
    for line in open(root_path + "all_restaurants_sf_r1000", "r"):
        line_json = json.loads(line)
        print(line_json)
        break


def misc_script():
    body = JSONEncoder().encode({
      "query": {
        "bool": {
          "must": [
              {
                  "match": {
                      "title":   "apocalypse now"
                  }
              }
          ],
        }
      }
    })

    body_json = json.loads(body)
    es = Elasticsearch(hosts="http://localhost:9200")
    results = es.search(body=json.loads(body_json))
    print results


# lat: [37.636529, 37.806258]
# log: [-122.360573, -122,513008]

if __name__ == '__main__':
    # get_all_restaurants_in_sf()
    # process_all_restaurant_file()
    get_all_restaurants_details()
    # index_restaurants_to_es()