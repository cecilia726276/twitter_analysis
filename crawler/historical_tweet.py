from tweepy import OAuthHandler
from tweepy import API
from tweepy import Cursor
import tweepy
import time,json,sys
import couchdb

# consumer_key = "gsdglK0s5hEEHs9VTxZ4W5364"
# consumer_secret = "7L2RVKUB975t3zV1jMVMd8kHAk4UlQ1qJSAyX7aEQ6ZgqKEHdg"
# access_token = "1124697978453684224-j7rnUDAY2WSFePjI1T0yYHFKpnaovJ"
# access_token_secret = "lEwYrJyMlW6s63jJ7N3OkSdAPggLMad3a7fiSs8azSvSv"

consumer_key = "9TrIboUD3Ato8fCkA1unnkTaz"
consumer_secret = "40hDJNHFwG7ZsrYqdNBwlNOBPdpXP6QUR3UzP2iAjjlAnugGIx"

access_token = "1124943135606370306-B3VEQwfh5je2wtWenWpmJ45pKX4KEY"
access_token_secret = "yvIEgCSF9Qppyd2OkeZoSN53pHjZIzfdWJQFngwYKiKas"

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = API(auth)
server = couchdb.Server('http://' + 'admin' + ':' + 'admin' + '@' + '45.113.233.208:32771/')
#db = couch['historical_twitter']
# For loop to iterate over tweets with #ocean, limit to 10
db_name = "history_twitter"



def read_file(filename):
    list = []
    with open(filename, "r") as file:
        for line in file:
            list.append(line.strip("\n"))
    return list

def crawler(keywords,db):#, places):
    docs_list = []
    for word in keywords:
        print(word)

        for tweet in tweepy.Cursor(api.search,
                                   q=word,
                                   geocode='-37.434005,144.494763,2000km'
                                   ).items():
            try:
                twitter_json = tweet._json

                if twitter_json['coordinates'] != None or twitter_json['user']['location'] != None:
                    # for place in places:
                    #     low_loc = place.lower(twitter_json['user']['location'])
                        #if place in low_loc:
                    doc = {"_id": twitter_json['id_str'],
                    "content": twitter_json['text'],
                    "coordinates": twitter_json["coordinates"]["coordinates"] if twitter_json["coordinates"] else None,
                    "location": twitter_json['user']["location"],
                    "when": twitter_json['created_at']}
                    docs_list.append(doc)
                    db.save(doc)
                    print(doc)

            except BaseException as e:
                print(e)
                time.sleep(3)
            except couchdb.http.ResourceConflict:
                 # handles duplicates
                time.sleep(3)
            # try:
            #     json_dict = json.loads(raw_status)
            #     doc = {
            #         "time": json_dict["created_at"],
            #         "id": json_dict["id"],
            #         "text": json_dict["text"],
            #         "location": json_dict["user"]["location"],
            #         # "coordinates": tweet.coordinates
            #     }
            #
            #     print(doc)
            # docs_list.append(doc)
            # db.save(doc)


    return docs_list

if __name__ == '__main__':
    keywords = read_file("food_keywords.txt")
    #places = read_file("victoria_regions.txt")
    for line in keywords:
        print(line)
    #locations = read_file("victoria.txt")
    if db_name not in server:
        db = server.create(db_name)

    db = server['history_twitter']

    t_list = crawler(keywords,db)#,places)

    #resultList = db.update(t_list)
    #print(resultList)
    # list = crawler()
    # print(len(list))


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