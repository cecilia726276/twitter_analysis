import couchdb
import json


server = couchdb.Server("http://admin:admin@45.113.233.208:5984/")

db_name = "processed_tweets"
outcome_db_name = "au_outcome"
states_name = ["NSW", "ACT", "VIC", "QLD", "SA", "WA", "TAS", "NT"]
db = server[db_name]
outcome_db = server[outcome_db_name]


def reduce(viewer_name):
    outcome = {}
    for item in db.view(viewer_name):
        if item.key not in outcome:
            outcome[item.key] = {"score": item.value, "count": 1}
        else:
            score = outcome[item.key]["score"]
            for element in score:
                score[element] += item.value[element]
            outcome[item.key]["count"] += 1
    for e in outcome:
        count = outcome[e]["count"]
        score = outcome[e]["score"]
        for element in score:
            score[element] = outcome[e]["score"][element] / count
    outcome_db.save(outcome)


if __name__ == '__main__':
    # if db_name not in server:
    #     db = server.create(db_name)

    views = {}

    for state in states_name:
        views[state] = {
            "map":
                '''
                function(doc){
                if(doc.state == ''' + "\"" + state + "\"" + '''
                && doc.status == true){
                emit(doc.state, doc.score);}
                } 
                '''
        }

        state_doc = {"_id": "_design/au_viewer",
                     "views": views}
    # state_doc = {"_id": "_design/processed_history_tweet_final_state_viewer",
    #              "views": views}

    # design_doc = {"_id": "_design/history_tweet_viewer",
    #               "views":{
    #                   "state_view": {
    #                       "map":
    #                           '''
    #                          function(doc){
    #                          if(doc.location == "Melbourne"){
    #                          emit(doc.location, doc);}
    #                          }
    #                         '''
    #                   }
    #               }}

    # state_doc = {
    #     "_id": "_design/processed_history_tweet_state_viewer",
    #     "views": {
    #         "all": {
    #             "map":
    #                 '''
    #                    function(doc){
    #                    if(doc.status == true){
    #                    emit(doc.state, doc);}
    #                    }
    #                   ''',
    #             "reduce":
    #                 '''
    #                     function(key, values, rereduce){
    #                     var outcome = {};
    #                     outcome.pos = sum(values.score.pos)/values.length;
    #                     outcome.neg = sum(values.score.neg)/values.length;
    #                     outcome.neu = sum(values.score.neu)/values.length;
    #                     return outcome;
    #                     }
    #                   '''
    #         }
    #     }
    # }

    vic_doc = {
        "_id": "_design/vic_viewer",
        "views": {
            "VIC": {
                "map":
                    '''
                       function(doc){
                       if(doc.state == "VIC" && doc.status == true){
                       emit(doc.new_location, doc.score);}
                       } 
                      '''
            }
        }
    }

    # design_doc = {"_id": "_design/processed_history_tweet_viewer",
    #               "views": {
    #                   "NSW_view": {
    #                       "map":
    #                           '''
    #                          function(doc){
    #                          if(doc.state == "NSW" && doc.status == true){
    #                          emit(doc.state, doc);}
    #                          }
    #                         '''
    #                   },
    #                   "ACT_view": {
    #                       "map":
    #                           '''
    #                          function(doc){
    #                          if(doc.state == "ACT" && doc.status == true){
    #                          emit(doc.state, doc);}
    #                          }
    #                         '''
    #                   },
    #                   "VIC_view": {
    #                       "map":
    #                           '''
    #                          function(doc){
    #                          if(doc.state == "VIC" && doc.status == true){
    #                          emit(doc.state, doc);}
    #                          }
    #                         '''
    #                   },
    #                   "QLD_view": {
    #                       "map":
    #                           '''
    #                          function(doc){
    #                          if(doc.state == "QLD" && doc.status == true){
    #                          emit(doc.state, doc);}
    #                          }
    #                         '''
    #                   },
    #                   "SA_view": {
    #                       "map":
    #                           '''
    #                          function(doc){
    #                          if(doc.state == "SA" && doc.status == true){
    #                          emit(doc.state, doc);}
    #                          }
    #                         '''
    #                   },
    #                   "WA_view": {
    #                       "map":
    #                           '''
    #                          function(doc){
    #                          if(doc.state == "WA" && doc.status == true){
    #                          emit(doc.state, doc);}
    #                          }
    #                         '''
    #                   },
    #                   "TAS_view": {
    #                       "map":
    #                           '''
    #                          function(doc){
    #                          if(doc.state == "TAS" && doc.status == true){
    #                          emit(doc.state, doc);}
    #                          }
    #                         '''
    #                   },
    #                   "NT_view": {
    #                       "map":
    #                           '''
    #                          function(doc){
    #                          if(doc.state == "NT" && doc.status == true){
    #                          emit(doc.state, doc);}
    #                          }
    #                         '''
    #                   }
    #
    #               }}
    if "_design/au_viewer" not in db:
        db.save(state_doc)
    if "_design/vic_viewer" not in db:
        db.save(vic_doc)

    # for s in states_name:
    #     reduce("au_viewer/"+s)
    # reduce("vic_viewer/VIC")


    # if "_design/processed_history_tweet_vic_viewer" not in db:
    #     db.save(vic_doc)

    # if "history_melbourne" not in server:
    #     newdb = server.create("history_melbourne")
    # else:
    # newdb = server['history_melbourne']


    # for item in db.view("processed_history_tweet_viewer/NSW_view"):
    #     print(item.key, item.id, item.value)

    # outcome = {}
    # for item in db.view("au_viewer/VIC"):
    #     if item.key not in outcome:
    #         outcome[item.key] = {"score": item.value, "count": 1}
    #     else:
    #         score = outcome[item.key]["score"]
    #         for element in score:
    #             score[element] += item.value[element]
    #         outcome[item.key]["count"] += 1
    # for e in outcome:
    #     count = outcome[e]["count"]
    #     score = outcome[e]["score"]
    #     for element in score:
    #         score[element] = outcome[e]["score"][element]/count
    #
    # print(outcome)

    # for item in db.view("processed_history_tweet_viewer/VIC_view"):
    #     print(item.key, item.id, item.value)
    # print(type(item.value))
    # del item.value['_rev']  #
    # newdb.save(item.value)

