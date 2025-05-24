import requests
import config

url = config.TEST_SERVER
data = {'key': 'test'}  # Словарь, который будет отправлен в теле POST
response = requests.post(url, data=data)
print(response.text)