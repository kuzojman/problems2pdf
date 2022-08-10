import requests
import json

with open('sample.json') as f:
    problems = json.load(f)

r = requests.post('http://127.0.0.1:5002', json=problems)
with open('request.pdf', 'wb') as f:
    f.write(r.content)