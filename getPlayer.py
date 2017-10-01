import time
import player
from slackclient import SlackClient



# connect
token = "xoxb-237318321376-yFZMOQoqAGKBuRD5O0vTkvo4"# found at https://api.slack.com/web#authentication
sc = SlackClient(token)
sc.rtm_connect()
# start reading
while True:
    print(sc.rtm_read())
    message = sc.rtm_read()
    print message[0]['type']=='message'
    time.sleep(1)

# read for users
# get or save user
# send message to slack
