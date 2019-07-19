import couchdb
from data_processing import data_process

user = "admin"
password = "admin"
server = couchdb.Server("http://" + user + ":" + password + "@" + "45.113.234.131:32773/")
old_db = server['historical_twitter']
new_db = server["new_tweets"]
# new_db = server["processed_tweets"]

counter = 0
for id in old_db:
    try:
        data = old_db[id]
        new_data = data_process.process_json(data)
    # new_db.save(data)
    # new_db.save(new_data)
        new_id = data["id"]
    except:
        print("Processing error")
    try:
        new_db[str(new_id)] = new_data
        print(new_data)
    except:
        print("Duplicate error.")

    # for element in data:
    #     print(type(element))
    #     print(element)
    # print(type(data))
    # print(data)
