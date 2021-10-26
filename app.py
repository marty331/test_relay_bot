import os
import logging
import ssl


if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
    ssl._create_default_https_context = ssl._create_unverified_context

from decouple import config

from slack_bolt import App
from flask import Flask, request
from slack_bolt.adapter.flask import SlackRequestHandler
# from slack import WebClient

logging.basicConfig(level=logging.DEBUG)

SLACK_BOT_TOKEN = config('SLACK_BOT_TOKEN')
SLACK_APP_TOKEN = config('SLACK_APP_TOKEN')
SLACK_SIGNING_SECRET = config('SLACK_SIGNING_SECRET')

# export SLACK_SIGNING_SECRET=***
# export SLACK_BOT_TOKEN=xoxb-***

# proxy_client = WebClient(
#     token=SLACK_BOT_TOKEN,
#     # proxy="http://proxy-am.shell.com:8080"
# )

app = App()

flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

# Add functionality here
@app.command("/hello-python")
def handle_message(body, say):
    # channel_id = "GUXKDKB3P" # basin_dna
    print(f"body {body}")
    channel_id = "GSXUDMJ2U" # old-xdigi-dev
    text = "Hello world!"
    # say(text=text, channel=channel_id)
    user_id = body["user_id"]
    say(f"Hi <@{user_id}>!")


# This will match any message that contains 👋
@app.message(":wave:")
def say_hello(message, say):
    user = message['user']
    say(f"Hi there, <@{user}>!")

# def main():
#     handler = SocketModeHandler(app, SLACK_APP_TOKEN)
#     handler.start()
#
# if __name__ == "__main__":
#     # Create an app-level token with connections:write scope
#     # handler = SocketModeHandler(app, SLACK_APP_TOKEN)
#     # handler.start()
#     main()

@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    return handler.handle(request)
