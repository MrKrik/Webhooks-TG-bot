import requests
import config as config

url = config.TEST_SERVER
data = {
    "action": "opened",
    "issue": {
     "url": "https://api.github.com/repos/octocat/Hello-World/issues/1347",
     "number": 1347,
    },
   "repository" : {
        "id": 1296269,
        "full_name": "octocat/Hello-World",
        "owner": {
            "login": "octocat",
            "id": 1,
        },
    },
   "sender": {
     "login": "octocat",
     "id": 1,
    }
}  
headers = {'Content-Type': 'application/json'}
response = requests.post(url, json=data, headers=headers)
print(response.text)