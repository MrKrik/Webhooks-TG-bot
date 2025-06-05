from quart import Quart, request
from bot.main import webhook_send
from aiogram.utils.markdown import link
import bot.db as db

app = Quart(__name__)

@app.route('/', methods=['POST'])
async def submit2():
    json_data = (await request.get_json())
    if db.get_message_settings(json_data["Id"]) == None:
        return
    content_type = request.headers.get('content-type')
    if (content_type == 'application/json'):
        commitAuthor = json_data["author"]
        commitAuthor_link = json_data["author_url"]
        commitAuthor = link(commitAuthor, commitAuthor_link)
        # changesurl = json_data['head_commit']['url'] response = f'{commitAuthor}\n{message}\n{comment}\n{changesurl}'
        comment = json_data['comment']
        message = json_data["message"]
        response = f'{commitAuthor}\n{message}\n{comment}\n'
        message_settings = db.get_message_settings()
        await webhook_send(text=response, channel_id=message_settings['channel_id'], thread_id=message_settings['thread_id'])

    
if __name__ == "__main__":
    app.run()
