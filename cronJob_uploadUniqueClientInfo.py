import os
import json
import requests

import time
import pandas as pd
import datetime

import argparse

from ibmcloudant.cloudant_v1 import CloudantV1, Document, BulkDocs
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

import logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()

from dotenv import  load_dotenv

load_dotenv()

credentials = {'CLOUDANT_API_KEY':os.environ.get("CLOUDANT_API_KEY"),
                'CLOUDANT_URL':os.environ.get("CLOUDANT_URL")}
        
ct = datetime.datetime.now()
logger.info("current time:-", str(ct))
authenticator = IAMAuthenticator(apikey=credentials['CLOUDANT_API_KEY'])

# Create an instance of the Cloudant service with the authenticator
service = CloudantV1(authenticator=authenticator)
service.set_service_url(credentials['CLOUDANT_URL'])

# Define a function to send a POST request with JSON data
def send_post_request(url, data, headers):
    data_json = json.dumps(data)
    response = requests.post(url, data=data_json, headers=headers)
    return response.json() #esponse.status_code, 

def read_csv_clients(src_path):
    dtype_dic= { 'NUMBER':str, }
    df = pd.read_csv(src_path,dtype = dtype_dic)
    return df.NUMBER.values.tolist()

def get_client_data(src_path):

    client_ids = read_csv_clients(src_path)
    logger.info(client_ids)
    # Define the URL
    url = os.environ.get("DISTRIBUTORS_URL")
    # Define the headers
    headers = {
        "Content-Type": "application/json"
    }
    # Create a list of JSON data for each POST request
    payloads= [ {
        "name": "",
        "number": f"{str(client_id)}",
        "id_branch": "",
        "id_credit_score": "",
        "city": "",
        "state": "",
        "limit": "",
        "page": ""
    } for client_id in client_ids
    ]

    responses = []

    for payload in payloads:
        try:
            response = send_post_request(url, payload, headers) 
        except:
            response =  f"Client data: Error getting data for {payload}" 
        responses.append(response)
    # logging.debug("responses", responses)
    return responses #responses.status_code

def get_credit_data(src_path):
    client_ids = read_csv_clients(src_path)
    # Define the URL

    url = os.environ.get("CREDIT_URL")

    # Define the headers
    headers = {
        "Content-Type": "application/json"
    }

    # Create a list of JSON data for each POST request
    payloads= [ {
        "number": f"{str(client_id)}",
        "date": ""
                 } 
                for client_id in client_ids 
                ]

    responses = []

    for payload in payloads:
        print(payload)
        try:
            response = send_post_request(url, payload, headers) 
        except:
            response = f"Credit data: Error getting data for {payload}" 
        responses.append(response)

    return responses 


def save_data_Cloudant(client_APIdata: list, credit_APIdata:list, prod:bool):
    # ct stores current time
    ct = datetime.datetime.now()
    logger.info("current time:-", str(ct))

    logger.info(client_APIdata, credit_APIdata)
    records = []
    for client, credit in zip(client_APIdata, credit_APIdata):
        # logger.info(client)
        client_credit = (client, credit) 

        logger.debug("client_credit tuple", client_credit)
        logging.debug("client credit 0",client_credit[0])
        document: Document = Document()
        document.Type = "Cliente"
        document.Record = {
            "upload_ts": ct.isoformat(),
            "auth": False,
            "satisfaction": 0,
            "id": client_credit[0]["distributors"][0]["number"],#str(id),#
	        "name": client_credit[0]["distributors"][0]["distributor"],
            "location": client_credit[0]["distributors"][0]["branch"],
            "phone_number": client_credit[0]["distributors"][0]["phones"][0]["number"],
            "credit_footwear": client_credit[1]["available_footwear"],
            "credit_financial": client_credit[1]["available_financial"],
            "credit_personal": client_credit[1]["available_credit_line"],
            "benefits": client_credit[1]["insurance_benefits"],
            "toPay": client_credit[1]["released"],
            "discount": client_credit[1]["discount"],
            "toPayAfterDiscount": client_credit[1]["toPay"],
            "cutoff_date": client_credit[1]["cutoff_date"],
            "should_pay_by": client_credit[1]["payment_date"]
                }
        records.append(document)
    # logger.info("records:", records)
    if prod:
        bulk_docs = BulkDocs(docs=records)
        response = service.post_bulk_docs(
            db="historico", bulk_docs=bulk_docs).get_result()
        logger.info(response)
    else: 
        bulk_docs = BulkDocs(docs=records)
        response = service.post_bulk_docs(
            db="test-historico", bulk_docs=bulk_docs).get_result()
        logger.info(response)
        
def delete_all_documents(prod):
    if prod:
        db_name = 'distribuidores'
    else:
        db_name = 'test-distribuidores'
    documents = service.post_all_docs(db=db_name).get_result()
    # Delete each document
    for doc in documents['rows']:
        doc_id = doc['id']
        logger.info(doc_id)
        if "_design" in doc_id:
                continue
        else:
            rev = doc['value']['rev']

            # Delete the document
            response = service.delete_document(
                db=db_name,
                doc_id=doc_id,
                rev=rev
            ).get_result()
            time.sleep(0.1)
            logger.info(f"Deleted document {doc_id} - {response}")

def get_unique_clients_latest_data(prod):
    if prod:
        db_name_all_docs = 'historico'
        db_name_only_distr = 'distribuidores'
    else:
        db_name_all_docs = 'test-historico'
        db_name_only_distr = 'test-distribuidores'
        
    response = service.post_all_docs(
        db=db_name_all_docs,
        include_docs=True,
        ).get_result()
        
    docs = []
    for item in response['rows']:
        if 'Record' in item['doc']:
            docs.append(item['doc']['Record'])
            
    df = pd.DataFrame(docs)
    
    # # ### filter
    df['upload_ts'] = pd.to_datetime(df['upload_ts'])

    df['date'] = df['upload_ts'].dt.date
    # max_date = df['date'].max()
    unique_ids_docs = df[df['upload_ts'] == df['upload_ts'].max()]
    unique_ids_docs['upload_ts'] = unique_ids_docs['upload_ts'].astype(str)
    unique_ids_docs['date'] = unique_ids_docs['date'].astype(str)

    logger.info(unique_ids_docs)
    bulk_docs = BulkDocs(docs=unique_ids_docs.to_dict(orient='records'))
    logger.info(bulk_docs)
    response = service.post_bulk_docs(
        db=db_name_only_distr, bulk_docs=bulk_docs).get_result()
    
# var/sftp/uploads/
def main():
    # Configure logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()

    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Script for production and non-production flags')
    parser.add_argument('--prod', action='store_true', help='Run in production mode')
    parser.add_argument('--nonprod', action='store_true', help='Run in non-production mode')
    args = parser.parse_args()

    if args.prod and args.nonprod:
        logger.info("Error: Both production and non-production flags cannot be specified simultaneously.")
        return

    if args.prod:
        logger.info("Running in production mode")
        src_path = r"/home/sftp_dportenis/DISTRIBUIDORES.csv"
    elif args.nonprod:
        logger.info("Running in non-production mode")
        src_path = r"test.csv"
    else:
        logger.info("No mode specified. Use either --prod or --nonprod.")
        return

    # Get client and credit data
    client_data = get_client_data(src_path)
    credit_data = get_credit_data(src_path)

    # Save historical data
    save_data_Cloudant(client_data, credit_data, args.prod if args.prod else args.nonprod)

    # Delete current distribuidores db
    delete_all_documents(args.prod if args.prod else args.nonprod)

    # Get most recent data from historic db and save unique to distribuidores db
    get_unique_clients_latest_data(args.prod if args.prod else args.nonprod)

if __name__ == "__main__":
    main()