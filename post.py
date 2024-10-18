import requests

url = 'http://localhost:5000/webhooks'
data = {'key': 'value'}  # Словарь, который будет отправлен в теле POST
response = requests.post(url, data=data)
print(response.text)