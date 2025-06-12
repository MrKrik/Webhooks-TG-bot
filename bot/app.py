from quart import Quart, request
from main import webhook_send
from aiogram.utils.markdown import link
import db 

app = Quart(__name__)

@app.route('/', methods=['POST'])
async def submit2():
    json_data = (await request.get_json())
    print(json_data)
    if db.get_message_settings(json_data["Id"]) == None:
        return "Broken id"
    content_type = request.headers.get('content-type')
    if (content_type == 'application/json'):
        commitAuthor = json_data["author"]
        commitAuthor_link = json_data["author_url"]
        commitAuthor = link(commitAuthor, commitAuthor_link)
        # changesurl = json_data['head_commit']['url'] response = f'{commitAuthor}\n{message}\n{comment}\n{changesurl}'
        comment = json_data['comment']
        message = json_data["message"]
        response = f'{commitAuthor}\n{message}\n{comment}\n'
        message_settings = db.get_message_settings(json_data["Id"])
        await webhook_send(message=response, channel_id=message_settings['channel_id'], thread_id=message_settings['thread_id'])
    return "fine"
    
if __name__ == "__main__":
    app.run()
