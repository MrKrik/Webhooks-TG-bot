import pymongo
from quart import Quart, request
# app = Quart(__name__)    

client = pymongo.MongoClient("localhost", 27017)
Git = client["GitHook-db"]
coll_webhooks = Git["Webhooks"]

def add(url, channel_id, thread_id, secret):
    coll_webhooks.insert_one({'url':url, 'channel_id': channel_id, 'thread_id':thread_id, 'secret':secret})

def get_message_settings(url):
    return coll_webhooks.find_one({'url':url},{'channel_id': 1,'thread_id': 1})




# def create(x):
#     print(x)
#     new_url = ""
#     max_id = -1
#     a = coll_webhooks.find()
#     for i in a:
#         if i["state"] == "available":
#             new_url = i["url"]
#             coll_webhooks.update_one(i, {"$set": {"state" : "unavailable", "id_user" : x}})
#             break
#         else:
#             max_id_db = i["_id"]
#             if max_id < max_id_db:
#                 max_id = max_id_db

#     if new_url != "":
#         return new_url 
    
#     else:           
#         new_id = max_id+1
#         new_url = f"http://127.0.0.1:5000/webhooks/{new_id}"
#         b = {"_id": new_id, "url" : new_url, "state" : "unavailable", "id_user" : x}
#         coll_webhooks.insert_one(b)
#         return new_url

# def show(x):
#     y = []
#     a = coll_webhooks.find()
#     for i in a:
#         if i["id_user"] == x:
#             y.append(i["url"])
#     return y

# def delete_webhooks(x, y):
#     coll_webhooks.update_one({"url" : x, "id_user" : y}, {"$set": {"state" : "available", "id_user" : ""}})

# app.run()
# def create(x):
#     max_id = -1
#     a = col_webhooks.find()
#     for i in a:
#         max_id_db = i["_id"]
#         state = i["state"]
#         if max_id < max_id_db and state != "unavailable":
#             max_id = max_id_db

#     new_id = max_id+1
#     new_url = f"http://127.0.0.1:5000/webhooks/{new_id}"
#     b = {"_id": new_id, "url" : new_url, "state" : "unavailable", "id_user" : x}
#     col_webhooks.insert_one(b)
#     return new_url
