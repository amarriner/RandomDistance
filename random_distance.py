import json
import keys
import locale
import math
import os
import random
import requests
import string
import twitter
import urllib

# Number of places to get from Google API
MAX_PLACES                  = 2

# List to store places
PLACES                      = []

# Number of times to attempt retrieval of a city from Google API
MAX_RETRIES                 = 10

# Working directory
pwd                         = '/home/amarriner/python/random-distance/'

# Used to pull random cities 
google_autocomplete_URL     = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?' + \
                                  'sensor=false&'                                             + \
                                  'types=(cities)&'                                           + \
                                  'key=' + keys.google_api_key + '&'                          + \
                                  'input='

# Gets specific data on a particular city
google_places_URL           = 'https://maps.googleapis.com/maps/api/place/details/json?'      + \
                                  'sensor=false&'                                             + \
                                  'key=' + keys.google_api_key + '&'                          + \
                                  'reference='

# Builds the map image
google_static_maps_URL      = 'http://maps.googleapis.com/maps/api/staticmap?'                       + \
                                  'sensor=false&'                                                    + \
                                  'size=640x480&'                                                    + \
                                  'format=png&'                                                      + \
                                  'markers=color:0x2222dd|label:1|<P1>&'                             + \
                                  'markers=color:0x2222dd|label:2|<P2>&'                             + \
                                  'path=geodesic:true|color:0x0000ff60|weight:4|<P1>|<P2>'

# Builds the name of the place that will be tweeted from place results
def build_name(place):
   return place['address_components'][0]['short_name'] + ' ' + \
          place['address_components'][len(place['address_components']) - 1]['long_name']

# Gets the distance between two latitude/longitude points using the haversine formula
# Taken from http://www.movable-type.co.uk/scripts/latlong.html
def get_distance(first_place, second_place):
   
   # Approximate radius of the earth in km
   radius = 6371

   delta_lat = math.radians( first_place['geometry']['location']['lat'] - \
                            second_place['geometry']['location']['lat'])
   delta_lng = math.radians( first_place['geometry']['location']['lng'] - \
                            second_place['geometry']['location']['lng'])

   first_lat_radians  = math.radians( first_place['geometry']['location']['lat'])
   second_lat_radians = math.radians(second_place['geometry']['location']['lat'])

   a = math.sin(delta_lat / 2) * math.sin(delta_lat / 2) + \
       math.sin(delta_lng / 2) * math.sin(delta_lng / 2) * \
       math.cos(first_lat_radians) * math.cos(second_lat_radians)

   c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

   return int(math.floor(radius * c))


# Retrieves random geo information on a place from Google API
def get_place():

   # Get a random string of three characters
   prefix = random.choice(string.letters) + random.choice(string.letters) + random.choice(string.letters)

   # Pull google places via the autocomplete API using the random string
   print 'Retrieving google autocomplete data with prefix ' + prefix + '...'
   request = requests.get(google_autocomplete_URL + prefix)
   places = json.loads(request.content)
   print 'Found ' + str(len(places['predictions'])) + ' places...'

   try:
      # Get data specific to a random place in the autocomplete results 
      print 'Retrieving google places data...'
      request = requests.get(google_places_URL + random.choice(places['predictions'])['reference'])
      place = json.loads(request.content)['result']
   except IndexError:
      return None
   else:
      return place

# Try to get as many places from Google API as is defined by MAX_PLACES
def get_places():
   for i in range(0, MAX_PLACES):    
      place = None
      retries = 0
   
      # Try to find a random place. Retry only MAX_RETRIES times before quitting
      while (place == None and retries < MAX_RETRIES):
         retries += 1
         print 'Attempting to find a random place (attempt ' + str(retries) + ')...'
         place = get_place()

      if place != None:
         PLACES.append(place)


# Attempt place retrieval
get_places()

# Make sure we've retrieved all the places we want
if len(PLACES) == MAX_PLACES:

   # Build tweet text
   tweet = 'The distance between ' + build_name(PLACES[0])         + \
           ' and ' + build_name(PLACES[1])                         + \
           ' is ' + str(get_distance(PLACES[0], PLACES[1])) + 'km' + \
           ' #Maps #GIS #Earth'

   # Debug output
   print('First : ' + build_name(PLACES[0]) + ' '            + \
         str(PLACES[0]['geometry']['location']['lat']) + ',' + \
         str(PLACES[0]['geometry']['location']['lng']))

   print('Second: ' + build_name(PLACES[1]) + ' '            + \
         str(PLACES[1]['geometry']['location']['lat']) + ',' + \
         str(PLACES[1]['geometry']['location']['lng']))

   print(tweet)
   print('Number of characters: ' + str(len(tweet)))

   # Download static image from Google API call
   urllib.urlretrieve(google_static_maps_URL.replace('<P1>', str(PLACES[0]['geometry']['location']['lat']) + ',' + \
                                                             str(PLACES[0]['geometry']['location']['lng']))        \
                                            .replace('<P2>', str(PLACES[1]['geometry']['location']['lat']) + ',' + \
                                                             str(PLACES[1]['geometry']['location']['lng']))        \
                                            , pwd + 'downloaded_map.png')

   # Connect to Twitter
   api = twitter.Api(keys.consumer_key, keys.consumer_secret, keys.access_token, keys.access_token_secret)

   # Post tweet text and image
   status = api.PostMedia(tweet, pwd + 'downloaded_map.png')

else:
   print "*** Error selecting places from Google! ***"
