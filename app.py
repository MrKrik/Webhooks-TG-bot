from quart import Quart, request
from main import webhook_test

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
        print((await request.get_json()))
        print(name)
        await webhook_test(name)
        # f
    else:
        name = (await request.form)['key']
        # Передача в бота
        await webhook_test(name)
        print(name)
    return f'Hello, {name}'

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
