import couchdb
server = couchdb.Server('http://admin:admin@45.113.234.131:32773/')
# The aurin vic data
db_name = "aurin"
# The aurin au data
db02_name = "aurin_au_data"
# The final outcome of tweet analysis
outcome_name = "au_outcome"

db = server[db_name]
db02 = server[db02_name]
outcome = server[outcome_name]
for _id in outcome:
    data = outcome[_id]
    print(data)

for _id in db02:
    data = db02[_id]
    print(data)

for item in db.view("aurin_vic_viewer/VIC_obesity_view"):
    print(type(item))
    print(item.key, item.id, item.value)

for item in db.view("aurin_vic_viewer/VIC_overweight_view"):
    print(type(item))
    print(item.key, item.id, item.value)
