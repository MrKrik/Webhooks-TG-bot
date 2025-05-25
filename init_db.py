import pymongo
import tests.config as config

client = pymongo.MongoClient(config.DB_URL)
Git = client["GitHook-db"]
coll_webhooks = Git["Webhooks"]

def create():
    coll_webhooks.insert_one({'field':'value'})
    coll_webhooks.delete_one({'field':'value'})
    print('База успешно создана')

create()