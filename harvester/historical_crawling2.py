from tweepy import OAuthHandler
from tweepy import API
import tweepy
import time,json,sys
import couchdb
import math

# permission key of crawling data from twitter
consumer_key = "vHxuKb8d7NVXHcdTkiZbSzLSi"
consumer_secret = "xutYW56NK1rV7rGqgnDOaVxjfYzuEOSuSPL59ogOrVmZeIVo9L"
access_token = "754801501629849600-ttzeIFmknQkLWM1btGdC38O59m39TEx"
access_token_secret = "WT7mqV1hQYxIpOamiYRF8WmVyk5qaoT1E0luyWrOOgW7t"
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
i = math.floor(len_lines/2)+1
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
        if i < len_lines-1:
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