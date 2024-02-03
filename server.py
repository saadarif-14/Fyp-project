import json
import logging
import threading
import time
from flask import Flask, request
import openai
import slack
from slackeventsapi import SlackEventAdapter
import pandas as pd
from datetime import datetime
from pandas import DataFrame
import schedule
from slack_sdk.errors import SlackApiError
from slack_sdk.web import WebClient
from slack_sdk.signature import SignatureVerifier
from slack_sdk.web.slack_response import SlackResponse
import os
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
import csv
from threading import Thread

channel_id = 'C06B1TGP06B'
# user_id = ''
# username = ''
user_input = ''
openai.api_key = os.environ['OPENAI_API_KEY']

# initiating logs file
logging.basicConfig(filename='bot_log.txt', level=logging.DEBUG)

# initiating slack web client
client = slack.WebClient(token='xoxb-6375933882199-6513079484240-uIL8A9voHQzWtuCzSW3zwhOJ')
BOT_ID = client.api_call("auth.test")['user_id']
verifier = SignatureVerifier('e71e28e7533add74fc08c3f20196d0e4')

# starting flast server and subscribing to events
app = Flask(__name__)
slack_event_adapter = SlackEventAdapter('e71e28e7533add74fc08c3f20196d0e4', '/slack/events', app)


@slack_event_adapter.on("message")
def handle_message(payload):
    event = payload.get('event', {})
    print(event)
    channel_id = event.get('channel')
    user_id = event.get('user')
    user_input = event.get('text')
    print(channel_id,user_id,user_input)

processed_events = set()

def schedule_send_survey():
    while True:
        try:
            # response = schedule.every().second.do(send_survey, channel_id)
            response = schedule.every().day.at('18:54').do(send_survey, channel_id)
            print("Scheduler Response:", response)
        except SlackApiError as e:
            logging.error(f"Error scheduling survey: {e.response['error']}")
            return False
        print("Scheduler thread is running :))) \n\n")
        time.sleep(1)

def survey_questions():
    return 'How was your performance today?'

def send_survey(channel_id):
    text = survey_questions()
    print("Send Survey called")
    try:
        response = client.chat_postMessage(
            channel=channel_id, text = "Hey"
        )
        print("Send Survey Response:", response)
    except SlackApiError as e:
        logging.error(f"Error sending survey: {e.response['error']}")


if __name__ == "__main__":
    
    print("Starting thread to send scheduled messages . . . .")
    schedule_send_survey()
    # schedule_thread = threading.Thread(target=schedule_send_survey)
    # schedule_thread.start()
    
    # print("Starting flask server . . . ")

    # app.run(debug=True, port=3000)
    print("Shutting down server\n . . . . \n . . ..  \n . .. ")