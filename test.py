import requests

BASE="http://127.0.0.1.5001/"

response=requests.post(BASE + "/helloworld/tim")
print(response.json())