import couchdb
import json
import re
# user = "admin"
# password = "admin"
server = couchdb.Server("http://" + "admin" + ":" + "admin" + "@" + "45.113.234.131:32773/")
new_db01 = server["aurin"]
new_db = server["aurin_au_data"]


content = ""
with open("aurin_final.json") as doc:
    for word in doc:
        content = word



str_dict = json.loads(content)
lga_lists = str_dict['features']
for lga_element in lga_lists:
    upload = lga_element["properties"]
    name = upload["lga_name"]
    processed_name = re.sub(u"\ \(.*?\\)|\\{.*?}|\\[.*?]", "", name)
    upload["lga_name"] = processed_name
    print(lga_element["properties"])
    new_db01.save(lga_element["properties"])

document = [{"state": "NSW", "overweight": 34.4020134, "obesity": 33.3375839},
            {"state": "ACT", "overweight": 39.3, "obesity": 24.2},
            {"state": "NT", "overweight": 35.88, "obesity": 33.24},
            {"state": "QLD", "overweight": 33.1113636, "obesity": 34.1340909},
            {"state": "SA", "overweight": 34.7450704, "obesity": 32.4802817},
            {"state": "TAS", "overweight": 34.7403226, "obesity": 29.2274194},
            {"state": "VIC", "overweight": 36.6518987, "obesity": 29.4797468},
            {"state": "WA", "overweight": 34.7513699, "obesity": 29.6931507}]

for doc in document:
    new_db.save(doc)
