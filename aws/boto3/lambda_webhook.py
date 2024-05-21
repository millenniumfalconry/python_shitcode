import logging
import json
import os
import requests
from laceworksdk import LaceworkClient

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    logger.info('Retrieved new message!')
    logger.info("Event: " + str(event))
    logger.info("Context: " + str(context))

    logger.debug('Load body')
    data=event.get('body')
    logger.info("Body: " + str(data))
    if data == "" or data is None:
        #Set the data to a default value
        data={}

    logger.debug('Load filter')
    filter=load_parameter(event, 'filter')
    if filter == "" or filter is None:
        #Set filter default behavior to always forward if it's not already set
        logger.info("Filter not configured") 
        filter={"operator": "true"}
    else:
        logger.info("Filter: " + str(filter)) 


    # Instantiate a LaceworkClient instance
    try:
        lacework_client = LaceworkClient(account=os.environ['LW_ACCOUNT'],
                    api_key=os.environ['LW_API_KEY'],
                    api_secret=os.environ['LW_API_SECRET'])
    except Exception as e:
        logger.error(f'Unable to configure Lacework client: {e}')
        
    #Collect Alert Details
    try: 
        alertDetails = lacework_client.alerts.get_details("51645", "Details")
        #data['event_id']
        #merge alertDetails with data
        data=alertDetails
    except Exception as e:
        logger.error(f'Alert Details search failed: {e}')
    
    logger.debug('Load Webhook URL')
    webhookUrl=load_parameter(event, 'webhookurl')
    logger.debug(webhookUrl) 

    logger.debug('Load Webhook Username')
    webhookUsername=load_parameter(event, 'webhookusername')

    logger.debug('Load Webhook Password')
    webhookPassword=load_parameter(event, 'webhookpassword')

    logger.debug('Load http method used')
    httpMethod= event['requestContext']['http']['method']
    logger.debug(httpMethod)

    logger.debug('Parse filter')
    filter=parse_json(filter)
    logger.debug('Parse body')
    data=parse_json(data)

    logger.debug('Evaluate filter')
    result=eval_filter(filter, data)
    

#More intelligent data retrieval, used for parsing filter and ensuring the filter is configured correctly
def getJsonAttributeAndValidate(dataPayload, attribute):
    result=dataPayload.get(attribute)
    if result is None:
        raise Exception("Attribute \"" + attribute + "\" not found in payload: " + str(dataPayload))
    return result

def getField(field, data):
    #No data, return none
    if data is None:
        return None

    #Data is not a json object, return none
    if not isinstance(data, dict):
        return None
        
    dotPos=field.find(".")
    if dotPos < 0:
        return data.get(field)
    else:
        firstField=field[0:dotPos]
        remainingField=field[dotPos+1:]
        return getField(remainingField, data.get(firstField))

def eval_equals(filter, data):
    field=getJsonAttributeAndValidate(filter, 'field')
    expectedValue=getJsonAttributeAndValidate(filter, 'value')
    actualValue=getField(field, data)
    return expectedValue == actualValue

def eval_contains(filter, data):
    field=getJsonAttributeAndValidate(filter, 'field')
    expectedValue=getJsonAttributeAndValidate(filter, 'value')
    actualValue=getField(field, data)
    
    if actualValue is None:
        return False
    else:
        return expectedValue in actualValue

def eval_in(filter, data):
    field=getJsonAttributeAndValidate(filter, 'field')
    expectedValues=getJsonAttributeAndValidate(filter, 'values')
    actualValue=data.get(field)
    for v in expectedValues:
       if v == actualValue:
           return True
    return False

def eval_not(filter, data):
    f=getJsonAttributeAndValidate(filter, 'filter')
    return not eval_filter(f, data)

def eval_and(filter, data):
    filters=getJsonAttributeAndValidate(filter, 'filters')
    for f in filters:
       if not eval_filter(f, data):
           return False
    return True
    
def eval_or(filter, data):
    filters=getJsonAttributeAndValidate(filter, 'filters')
    for f in filters:
       if eval_filter(f, data):
           return True
    return False


    # Send SNS notification
    sns_client = boto3.client('sns')
    topic_arn = 'arn:aws:sns:us-east-1:123456789012:webhook-notification-topic'  # Replace with your SNS topic ARN
    message = 'Webhook payload received and processed successfully'
    
    sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )

    # Return a response
    response = {
        'statusCode': 200,
        'body': 'Webhook payload received and processed successfully'
    }

    return response


