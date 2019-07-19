import couchdb
import json

server = couchdb.Server('http://' + 'admin' + ':' + 'admin' + '@' + '45.113.234.131:32773/')
db_name = "aurin"
db02_name = "aurin_au_data"
states_name = ["nsw", "act", "vic", "qld", "sa", "wa", "tas", "nt"]

db = server[db_name]
design_doc = {"_id": "_design/aurin_vic_viewer",
              "views": {
                      "VIC_overweight_view": {
                          "map":
                              '''
                             function(doc){
                             if(doc.ste_name == "vic"){
                             emit(doc.lga_name, doc.ovrwgt_p_2_asr);}
                             }
                            '''
                      },
                      "VIC_obesity_view": {
                          "map":
                              '''
                             function(doc){
                             if(doc.ste_name == "vic"){
                             emit(doc.lga_name, doc.obese_p_2_asr);}
                             }
                            '''
                      }
                  }
              }
if "_design/aurin_vic_viewer" not in db:
    db.save(design_doc)


for item in db.view("aurin_vic_viewer/VIC_obesity_view"):
    print(type(item))
    print(item.key, item.id, item.value)

for item in db.view("aurin_vic_viewer/VIC_overweight_view"):
    print(type(item))
    print(item.key, item.id, item.value)
