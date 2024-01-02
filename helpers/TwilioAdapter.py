from twilio.rest import Client
import json
import load_dotenv
import os

class MessageClient:
    def __init__(self):
        print('Initializing messaging client')
        
        load_dotenv()

        twilio_number =     os.environ("TRIAL_NUMBER")
        twilio_account_sid =os.environ("TWILIO_ACCOUNT_SID")
        twilio_auth_token = os.environ("TWILIO_AUTH_TOKEN")
        self.twilio_number = twilio_number
        self.twilio_client = Client(twilio_account_sid, twilio_auth_token)

        print('Twilio client initialized')

    def send_message(self, body, to):
        self.twilio_client.messages.create(
            body=body,
            to="whatsapp:+52"+to,
            from_="whatsapp:"+self.twilio_number,
        )
