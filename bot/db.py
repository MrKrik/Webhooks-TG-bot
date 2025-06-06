import pymongo 
import os


client = pymongo.MongoClient(os.getenv("DB_URL"))
Git = client["GitHook-db"]
coll_webhooks = Git["Webhooks"]

def add(name, url, author_id,channel_id, thread_id, secret = None):
    coll_webhooks.insert_one({'webhook_name':name,'url':url, 'author_id':author_id,'channel_id': channel_id, 'thread_id':thread_id, 'secret':secret})

def get_message_settings(url):
    return coll_webhooks.find_one({'url':url},{'channel_id': 1,'thread_id': 1, '_id': 0})

def get_user_webhooks(user_id):
    return list(coll_webhooks.find({'author_id':user_id},{'webhook_name': 1, '_id': 0}))

def get_webhooks_info(webhook_name):
    webhook_data = list(coll_webhooks.find({'webhook_name':webhook_name},{'webhook_name': 1, 'url':1, 'author_id':1,'channel_id': 1, 'thread_id':1, '_id': 0}))[0]
    message = f"Название вебхука: {webhook_data['webhook_name']}\nUrl вебхука: {webhook_data['url']}\nId канала: {webhook_data['channel_id']}\nId ветки: {webhook_data['thread_id']}"
    return message

def delete_webhook(webhook_name):
    coll_webhooks.delete_one({'webhook_name':webhook_name})
