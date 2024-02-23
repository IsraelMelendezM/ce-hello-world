import csv
from ibm_watson import AssistantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import os
import csv 

from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("APIKEY_WA")
workspace_id = os.environ.get("WORKSPACE_ID")
url = os.environ.get("URL_WA")
# Set up authentication
authenticator = IAMAuthenticator(api_key)
assistant = AssistantV1(
    version='2021-06-14',
    authenticator=authenticator
)

assistant.set_service_url(url)

# Fetch all conversations
all_conversations = []

response = assistant.list_logs(
    workspace_id=workspace_id
).get_result()

all_conversations.extend(response['logs'])

# Fetch subsequent pages if available
while response.get('pagination') and response['pagination'].get('next_url'):
    response = assistant.list_logs(
        workspace_id=workspace_id,
        page_token=response['pagination']['next_url']
    ).get_result()
    all_conversations.extend(response['logs'])

# Write conversations to CSV
csv_file = 'conversations.csv'

with open(csv_file, 'a', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['conversation_id',
                                              'client_id', 
                                              'response_timestamp',
                                                'input_text',
                                                  'output_text'])
    
    # Check if file is empty and write header if needed
    if file.tell() == 0:
        writer.writeheader()
    
    # Write conversations to CSV
    for conversation in all_conversations:
        # data = json.loads(json_data)

        # Extracting relevant information
        input_text = conversation['request']['input']['text']
        response_text = conversation['response']['output']['text']
        id_cliente = conversation['request']['context']['ID_CLIENTE'] if 'ID_CLIENTE' in conversation['request']['context'].keys() else 'N/A'

        writer.writerow({
            'conversation_id': conversation['request']['context']['conversation_id'],
            'client_id': id_cliente,
            'response_timestamp': conversation['response_timestamp'],
            'input_text': input_text,
            'output_text': response_text
        })
