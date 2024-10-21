from quart import Quart, request
from main import webhook_send
from aiogram.utils.markdown import link
import db
from os import system


app = Quart(__name__)

@app.route("/")
async def hello():
    return "Hello World!"

@app.route('/webhooks/<webhookUrl>', methods=['POST'])
async def submit(webhookUrl):
    # Обработка запроса
    if db.get_message_settings(webhookUrl) == None:
        return
    content_type = request.headers.get('content-type')
    if (content_type == 'application/json'):
        name = request.headers.get('X-GitHub-Event')
        print(request.headers)
        json_data = (await request.get_json())
        commitAuthor = json_data['sender']['login']
        commitAuthor_link = json_data['sender']['html_url']
        commitAuthor = link(commitAuthor, commitAuthor_link)
        changesurl = json_data['head_commit']['url']
        comment = json_data['head_commit']['message']
        if json_data['created'] == True:
            message = "Создал ветку"
        else:
            message = 'Сделал push'
        response = f'{commitAuthor}\n{message}\n{comment}\n{changesurl}'
        message_settings = db.get_message_settings(webhookUrl)
        await webhook_send(text=response, channel_id=message_settings['channel_id'], thread_id=message_settings['thread_id'])

if __name__ == "__main__":
    app.run()
