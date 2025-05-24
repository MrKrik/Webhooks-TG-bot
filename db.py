import pymongo 
import config

client = pymongo.MongoClient(config.DB_URL)
Git = client["GitHook-db"]
coll_webhooks = Git["Webhooks"]

def add(name, url, author_id,channel_id, thread_id, secret = None):
    coll_webhooks.insert_one({'webhook_name':name,'url':url, 'author_id':author_id,'channel_id': channel_id, 'thread_id':thread_id, 'secret':secret})

def get_message_settings(url):
    print(coll_webhooks.find_one({'url':url},{'channel_id': 1,'thread_id': 1, '_id': 0}))
    return coll_webhooks.find_one({'url':url},{'channel_id': 1,'thread_id': 1, '_id': 0})

def get_user_webhooks(user_id):
    print(list(coll_webhooks.find({'author_id':user_id},{'webhook_name': 1, '_id': 0})))
    return list(coll_webhooks.find({'author_id':user_id},{'webhook_name': 1, '_id': 0}))

def get_webhooks_info(webhook_name):
    webhook_data = list(coll_webhooks.find({'webhook_name':webhook_name},{'webhook_name': 1, 'url':1, 'author_id':1,'channel_id': 1, 'thread_id':1, '_id': 0}))[0]
    message = f"Название вебхука: {webhook_data['webhook_name']}\nUrl вебхука: {webhook_data['url']}\nId канала: {webhook_data['channel_id']}\nId ветки: {webhook_data['thread_id']}"
    return message

def delete_webhook(webhook_name):
    coll_webhooks.delete_one({'webhook_name':webhook_name})





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
