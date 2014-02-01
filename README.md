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

#### Sample Tweet

<blockquote class="twitter-tweet" lang="en">
   <p>The distance between Yulin, Shaanxi, China and Attendorn, Germany is 7514km
   <a href="http://t.co/WGWpCDFhwm">pic.twitter.com/WGWpCDFhwm</a></p>
   &mdash; Random Distance (@RandomDistance) 
   <a href="https://twitter.com/RandomDistance/statuses/429433953599356929">February 1, 2014</a>
</blockquote> <script async src="//platform.twitter.com/widgets.js" charset="utf-8"></script>

#### Sample Map
 
![Sample Map](https://pbs.twimg.com/media/BfWn58NIQAAcB81.png "Sample Map")
