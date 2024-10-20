from quart import Quart, request
from main import webhook_test
from aiogram.utils.markdown import link

app = Quart(__name__)

@app.route("/")
async def hello():
    return "Hello World!"

@app.route('/webhooks', methods=['POST'])
async def submit():
    # Обработка запроса
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
        # await webhook_test(response)
    else:
        name = (await request.form)['key']
        # Передача в бота
        await webhook_test(name)
        print(name)
    return f'Hello, {name}'

@app.route('/webhooks/<pageID>', methods=['GET'])
async def testget(pageID):
    return pageID

print('''F
      f
      f
      f
      f
      f
      f
      ff
      f
      f
      f
      f
      f
      f
      ff
      f
      f
      f
      f
      f
      ff
      f
      ''')
if __name__ == "__main__":
    app.run(debug=True)
