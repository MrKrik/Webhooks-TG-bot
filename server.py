from quart import Quart, request
from main import webhook_test

app = Quart(__name__)

@app.route("/")
async def hello():
    return "Hello World!"

@app.route('/webhooks', methods=['POST'])
async def submit():
    # Обработка запроса
    name = (await request.form)['key']
    # Передача в бота
    await webhook_test(name)
    print(name)
    return f'Hello, {name}'

if __name__ == "__main__":
    app.run(debug=True)
