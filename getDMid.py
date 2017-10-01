import requests
r = requests.get('https://slack.com/api/im.list', auth = "xoxb-237318321376-yFZMOQoqAGKBuRD5O0vTkvo4",  )
print r.status_code
print r.text
