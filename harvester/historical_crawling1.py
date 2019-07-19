from tweepy import OAuthHandler
from tweepy import API
import tweepy
import time,json,sys
import couchdb
import math

# permission key of crawling data from twitter
consumer_key = "gsdglK0s5hEEHs9VTxZ4W5364"
consumer_secret = "7L2RVKUB975t3zV1jMVMd8kHAk4UlQ1qJSAyX7aEQ6ZgqKEHdg"
access_token = "1124697978453684224-j7rnUDAY2WSFePjI1T0yYHFKpnaovJ"
access_token_secret = "lEwYrJyMlW6s63jJ7N3OkSdAPggLMad3a7fiSs8azSvSv"
auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# the master node of couchdb
api = API(auth)
couch = couchdb.Server('http://' + 'admin' + ':' + 'admin' + '@' + '45.113.234.131:32773/')
# if the database already doesn't exist, then create
dbname = 'historical_twitter'
if dbname in couch:
    db = couch['historical_twitter']
else:
    db = couch.create('historical_twitter')

# Use search api to find the area with -29.154615,132.432475 as the center and 3500km as the radius
def search_tweets(tag):
    c = tweepy.Cursor(api.search,
                      q=tag,
                      geocode='-29.154615,132.432475,3500km',
                      include_entities=True
                      # geocode='1.3552217,103.8231561,50km'
                      ).items()
    return c

# search the key words in the fast food list
fopen = open('fastfood.txt','r')
lines = fopen.readlines()
food = []
for line in lines:
    line = line.strip('\n')
    food.append(line)
len_lines = len(lines)
# the start position of the third instance
i = 0
c = search_tweets(food[i])
while True:
    try:
        tweet = c.next()
        raw_status = json.dumps(tweet._json)
        json_dict = json.loads(raw_status)
        doc = {
            "_id": json_dict["id"],
            "content": json_dict["text"],
            "coordinates": json_dict["coordinates"],
            "location": json_dict["user"]["location"],
            "when": json_dict["created_at"]
            # "coordinates": tweet.coordinates
        }
        print(doc)
        db.save(doc)
    except tweepy.TweepError:
        # Sleep 15 minutes if the limit is reached
        print("sleeping......")
        time.sleep(60 * 15)
        continue
    except StopIteration:
        # Stop condition
        if i < math.floor(len_lines/2)-1:
            i = i + 1
            print(i)
            c = search_tweets(food[i])
            continue
        else:
            break
    except couchdb.http.ResourceConflict:
        print("repeated tweet")


# for tweet in Cursor(api.search,
#                     q='#ocean',
#                     since='2016-11-25',
#                     until='2016-11-27',
#                     geocode='1.3552217,103.8231561,100km',
#                     lang='fr').items(10):
#     try:
#         print(tweet)
#     except tweepy.TweepError as e:
#         print(e.reason)
#
#     except StopIteration:
#         break