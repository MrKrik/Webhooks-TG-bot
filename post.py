import requests

url = 'https://githook-bee-bot.amvera.io/webhooks'
data = {'key': 'test'}  # Словарь, который будет отправлен в теле POST
response = requests.post(url, data=data)
print(response.text)