import pymongo
import os

client = pymongo.MongoClient(os.getenv("DB_URL"))
Git = client["GitHook-db"]
coll_webhooks = Git["Webhooks"]

def create():
    coll_webhooks.insert_one({'field':'value'})
    coll_webhooks.delete_one({'field':'value'})
    print('База успешно создана')

create()