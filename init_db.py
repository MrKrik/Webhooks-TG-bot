import pymongo


client = pymongo.MongoClient('mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+2.2.6')
Git = client["GitHook-db"]
coll_webhooks = Git["Webhooks"]

def create():
    coll_webhooks.insert_one({'field':'value'})
    coll_webhooks.delete_one({'field':'value'})

def add(url, channel_id, thread_id, secret):
    coll_webhooks.insert_one({'url':url, 'channel_id': channel_id, 'thread_id':thread_id, 'secret':secret})

def get_message_settings(url):
    return coll_webhooks.find_one({'url':url},{'channel_id': 1,'thread_id': 1})\

message_settings = get_message_settings('f')
print(message_settings['channel_id'], message_settings['thread_id'])

# add('f', 555, 4, 'megapassword')