import json
import requests
import os
import boto3
from .extractors.clover_order_extractor import CloverOrderExtractor

def get_verification_code(webhook_message, Bucket):
    s3 = boto3.client('s3')
    fileName = 'verificationCode' + '.json'
    bucket = Bucket #TODO: Bucket name is hardcoded, need to change during deployment
    upload_file = bytes(json.dumps(webhook_message).encode('UTF-8'))
    s3.put_object(Bucket=bucket, Key=fileName, Body=upload_file)
def get_order_extraction_config(webhook_message: dict) -> list:
    merchant_id = list(webhook_message["merchants"].keys())[0] #TODO: for multiple merchants list indices need to be updated
    # TODO: for multiple providers need to handle merchant_ids and access_token in a different way
    return [{
        "merchant_id": merchant_id,
        "BaseUrl": "https://api.clover.com/v3/merchants",
        "http_method": "GET",
        "auth_mode": "Bearer",
        "auth_token": access_token #REPLACE YOUR TOKEN HERE
    }]


def lambda_handler(event, context=None):
    
    global extractor
    http_method = event["httpMethod"]
    if (http_method != "POST"):
        return {
            "statusCode": 400,
            "body": json.dumps({
                "message": "Bad Request",
                "description": f"{http_method}: Method not implemented",
            })
        }
    webhook_message = json.loads(event["body"])
    if("verificationCode" in webhook_message.keys()):
        get_verification_code(webhook_message)
        return {
            'statusCode': 200,
            'body': json.dumps("ok")
        }
    merchant_obj = webhook_message["merchants"]
    extraction_configs = get_order_extraction_config(webhook_message)
    for config in extraction_configs:
        extractor = CloverOrderExtractor(config)

    orders = []
    # TODO: for current scenario loop will run only at once as implementation is for a single merchant
    for mId in merchant_obj.keys(): #TODO: update get_order_extraction_config method for multiple merchant ids
        object_list = merchant_obj[mId]
        orders.append(extractor.get_live_orders(object_list))
#    TODO: Save access_token to minimize the multiple signin requests
    auth_payload = {
        "username": "UserName",
        "password": "Password"
    }

    auth_response = requests.post("https://api.example.com/user/signin", data=json.dumps(auth_payload))
    auth_json = json.loads(auth_response.text)
    token = auth_json["AuthenticationResult"]["IdToken"]
    headers = {
        "Authorization": f"Bearer {token}"
    }
    for order in orders:
        payload = json.dumps(order)
        x = requests.post('https://api.example.com/brand/1/store/1/order', headers=headers, data=payload)
        print("status_code:" + str(x.status_code))

    return {
        'statusCode': 200,
        'body': json.dumps("ok")
    }

