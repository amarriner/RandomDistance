# Random Distance Bot

*A twitter bot that tweets a map with random cities on it to [@RandomDistance](https://twitter.com/RandomDistance)*

This bot uses Google Places APIs to find two random cities on Earth and calculates the distance between them. It will then pull 
a static map via the Google Static Maps API and tweet everything it has accumulated. The distance calculation uses the haversine 
formula which I cribbed from [here](http://www.movable-type.co.uk/scripts/latlong.html).

**Dependencies**
 * Google API key and permissions from the [Google API Console](https://code.google.com/apis/console/)
 * [Twitter](https://dev.twitter.com/) consumer keys and access tokens
 * [python-twitter Module](https://github.com/bear/python-twitter)

**TODO**
 * Add more GIS data
 * Add weather data

#### Sample Map
 
![Sample Map](https://pbs.twimg.com/media/BfWn58NIQAAcB81.png "Sample Map")

