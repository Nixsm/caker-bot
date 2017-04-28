import os
from time import sleep
from slackclient import SlackClient

message = 'Hey %s! Welcome to the Baking a Caker group. Your first step to improve your technical skills and get ready for our selection process is to read this page on our WIKI: https://bakingacaker.sliki.io/baking-a-caker/doc/welcome-guidelines'

slack_token = os.environ.get("SLACK_BOT_TOKEN")
print("Starting Caker bot")

sc = SlackClient(slack_token)

def filter_events(events):
    for event in events:
        if event['type'] == 'team_join' and not event['user']['is_bot']:
            send_message(message, event)

def send_message(message, event):
    message_to_send = message % ('@' + event['user']['name'])
    send_slack_message(message_to_send, "#general")

def send_slack_message(message, channel):
    sc.api_call(
        "chat.postMessage",
        channel=channel,
        text=message,
        link_names="true",
        username="Caker Bot"
    )

if sc.rtm_connect():
    print("Caker bot Started")
    ignore_count = 0
    total_ignores = 5
    while True:
        events = []
        # ignore first five events because they are old
        # yes, this is a workaround
        if ignore_count < total_ignores:
            events = sc.rtm_read()
            ignore_count += 1
            continue
        filter_events(events)
        sleep(1)
else:
    print("Failed to start Caker Bot, your Slack token is probably wrong")
