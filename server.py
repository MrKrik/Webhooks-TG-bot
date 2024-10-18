from flask import Flask, request
from main import webhook_test

app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route('/webhooks', methods = ['POST'])
async def submit():
    # Обработка запроса
    name = request.form['key']
    # Передача в бота
    await webhook_test(name)
    print(name)
    return f'Hello, {name}'
    

if __name__ == "__main__":
    app.run(debug=True)