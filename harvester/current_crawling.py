from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import os
import sys
import time,json,sys
import couchdb

consumer_key = "9TrIboUD3Ato8fCkA1unnkTaz"
consumer_secret = "40hDJNHFwG7ZsrYqdNBwlNOBPdpXP6QUR3UzP2iAjjlAnugGIx"
access_token = "1124943135606370306-B3VEQwfh5je2wtWenWpmJ45pKX4KEY"
access_token_secret = "yvIEgCSF9Qppyd2OkeZoSN53pHjZIzfdWJQFngwYKiKas"
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# set up couchdb
# put in your own db name and address
couch = couchdb.Server('http://' + 'admin' + ':' + 'admin' + '@' + '45.113.234.131:32773/')
dbname = 'current_twitter'
if dbname in couch:
    db = couch['current_twitter']
else:
    db = couch.create('current_twitter')

class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
        This is a custom listener that just prints received tweets to stdout.
        """
    def on_data(self, data):
        try:
            json_dict = json.loads(data)
            doc = {
                "id": json_dict["id"],
                "content": json_dict["text"],
                "coordinates": json_dict["coordinates"],
                "location": json_dict["user"]["location"],
                "when": json_dict["created_at"]
            }
            print(doc)
            db.save(doc)
            # return True
        except BaseException as e:
            print(e)
            time.sleep(3)
        except couchdb.http.ResourceConflict:
            # handles duplicates
            time.sleep(3)


    def on_error(self, status_code):
        print(status_code)

fopen = open('fastfood.txt','r')
lines = fopen.readlines()
food = []
for line in lines:
    line = line.strip('\n')
    food.append(line)
print("Streaming starting......")
try:
    twitterStream = Stream(auth, StdOutListener())
    twitterStream.filter(track=food)
    twitterStream.filter(locations=[-37.020100, 144.964600])
except Exception as e:
    print (e)
    print("Error or execution finished. Program exiting... ")
    twitterStream.disconnect()