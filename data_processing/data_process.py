import nltk
import couchdb
nltk.download('vader_lexicon')
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import requests
import json
import re

# sentiment analyzer
analyzer = SentimentIntensityAnalyzer()
requestUrl = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input="
restUrl = "%20Australia&inputtype=textquery&fields=formatted_address,name,geometry&key="
# google map api key
api_key01 = "AIzaSyD3K3ulMIYyC2Anc8mDVdxg0gaqGNclLpY"
api_key02 = "AIzaSyBL9JHYPAHXJkPMp0DgKSrKusvFMUxvvxY"
# au postcode regex
au_postcode_regex = "^(0[289][0-9]{2})|([1345689][0-9]{3})|(2[0-8][0-9]{2})|(290[0-9])|(291[0-4])|(7[0-4][0-9]{2})|(" \
                    "7[8-9][0-9]{2})$ "
# state regex
state_regex = "([A-Z]{2,3})"
state_lists = ["New South Wales", "Australian Capital Territory", "Victoria", "Queensland", "South Australia", "Western Australia", "Tasmania", "Northern Territory"]
trie = []
with open("fastfood.txt") as dictionary:
    for word in dictionary:
        word = word.lower()[:-1]
        trie.append(word)

location_list = []
with open("VIC.txt") as vic:
    for word in vic:
        word = word[:-1]
        location_list.append(word)


def generate_request(location):
    request = requestUrl + location + restUrl + api_key01
    resp = requests.get(request)
    return resp.json()


def get_victoria_part(lat, lng):
    api_key = "AIzaSyC4XatT9vxskvkPJPaH8VYreC0Cq2eXD34"
    request_Url = "https://maps.google.com/maps/api/geocode/xml?key=" \
                  + api_key + "&latlng=" + str(lat) + "," + str(lng) + "&sensor=false"
    rst = str(requests.get(request_Url).content)
    for substring in location_list:
        if substring in rst:
            print(substring)
            return substring


# add new_coordinate, new_location, postcode, state to the output according to google map place api
def process_response(json_response, coordinates, doc):
    # see if the candidate is null
    if not json_response["candidates"]:
        doc["status"] = False
        return doc
    else:
        candidates = json_response["candidates"]
        for candidate in candidates:
            formatted_address = candidate["formatted_address"]
            if "Australia" not in formatted_address:
                continue
            else:
                doc["new_coordinate"] = candidate["geometry"]["location"]
                # if coordinates:
                #     #     doc["new_coordinate"]["lat"] = coordinates[1]
                #     #     doc["new_coordinate"]["lng"] = coordinates[0]
                #     if coordinates["type"] == "Point":
                #         doc["new_coordinate"]["lat"] = coordinates["coordinates"][1]
                #         doc["new_coordinate"]["lng"] = coordinates["coordinates"][0]

                doc["new_location"] = candidate["name"]
                if re.search(au_postcode_regex, formatted_address):
                    doc["postcode"] = re.search(au_postcode_regex, formatted_address).group(0)

                if re.search(state_regex, formatted_address):
                    doc["state"] = re.search(state_regex, formatted_address).group(0)
                    if "New South Wales" in formatted_address:
                        doc["state"] = "NSW"
                    if "Australian Capital Territory" in formatted_address:
                        doc["state"] = "ACT"
                    if "Victoria" in formatted_address:
                        doc["state"] = "VIC"
                    if "Queensland" in formatted_address:
                        doc["state"] = "QLD"
                    if "South Australia" in formatted_address:
                        doc["state"] = "SA"
                    if "Western Australia" in formatted_address:
                        doc["state"] = "WA"
                    if "Tasmania" in formatted_address:
                        doc["state"] = "TS"
                    if "Northern Territory" in formatted_address:
                        doc["state"] = "NT"
                    if doc["state"] == "VIC":
                        doc["new_location"] = get_victoria_part(candidate["geometry"]["location"]["lat"],
                                                                candidate["geometry"]["location"]["lng"])
                doc["status"] = True
                return doc
        doc["status"] = False
        return doc


# for processing the content
# do the sentiment analysis, return scores: neu, pos, neg
def process_content(content, doc):
    doc["content"] = content
    score = analyzer.polarity_scores(content)
    # del score["compound"]
    doc["score"] = score
    for substring in trie:
        if substring in content.lower():
            return doc
    doc["status"] = False
    return doc


def process_json(json_object):
    # extract coordinates
    # json_object = json.loads(res_string)
    del json_object["_rev"]
    try:
        if "location" not in json_object:
            json_object["status"] = False
            return json_object
    except:
        print("location error")
    try:
        resp = generate_request(json_object["location"])
    except:
        print("generate request error")

    try:
        json_object = process_response(resp, json_object["coordinates"], json_object)
    except:
        print("coordinates error")

    try:
        if not json_object["status"]:
            return json_object
    except:
        print("status coordinate error")
    # preprocessing: removing @ user, URL, hashtags
    try:
        if not json_object["content"]:
            if json_object["text"]:
                content = re.sub(r"http\S+|@\S+|[_#$%^&*()<>/|\'\\\}{~:,\.]", "", json_object["text"])
                json_object = process_content(content, json_object)
                del json_object["text"]
            else:
                json_object["status"] = False
                return json_object
        else:
            content = re.sub(r"http\S+|@\S+|[_#$%^&*()<>/|\'\\\}{~:,\.]", "", json_object["content"])
            json_object = process_content(content, json_object)
        del json_object["coordinates"]
        del json_object["location"]
    except:
        print("content error")
    return json_object


user = "admin"
password = "admin"
server = couchdb.Server("http://" + user + ":" + password + "@" + "45.113.234.131:32773/")
old_db = server['historical_twitter']
new_db = server["final_tweets"]
# new_db = server["processed_tweets"]

counter = 0
for id in old_db:
    try:
        data = old_db[id]
        new_data = process_json(data)
        if not new_data["status"]:
            break
    # new_db.save(data)
    # new_db.save(new_data)
        else:
            new_id = data["id"]
    except:
        print("Processing error")
    try:
        new_db[str(new_id)] = new_data
        print(new_data)
    except:
        print("Duplicate error.")

# process each json here
# with open("test.json", "rU") as whole_data:
#     # read the file line by line
#     for line in whole_data:
#         output = process_json(line)
#         print(output)
