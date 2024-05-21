import boto3

def get_s3_data_events(access_key_id, region):
    # create client
    cloudtrail_client = boto3.client('cloudtrail', region_name=region)

    # paginate results
    s3_events = []
    paginator = cloudtrail_client.get_paginator('lookup_events')
    for page in paginator.paginate(
        LookupAttributes=[
            {
                'AttributeKey': 'AccessKeyId',
                'AttributeValue': access_key_id
            },
            {
                'AttributeKey': 'EventSource',
                'AttributeValue': 's3.amazonaws.com'
            }
        ]
    ):
        # return relevant s3 results
        for event in page['Events']:
            bucket_name = parse_bucket_name(event)
            event_name = event['EventName']
            event_time = event['EventTime']
            user_identity = event.get('userIdentity', {})
            principal_id = user_identity.get('principalId', 'Unknown')
            user_name = user_identity.get('sessionContext', {}).get('sessionIssuer', {}).get('userName', 'Unknown')
            s3_events.append({
                'EventName': event_name,
                'EventTime': event_time,
                'PrincipalId': principal_id,
                'UserName': user_name,
                'BucketName' : bucket_name
            })

    return s3_events

def parse_bucket_name(event):
    # extract bucket name
    request_parameters = event.get('requestParameters', {})
    bucket_name = request_parameters.get('bucketName')
    return bucket_name or 'Unknown'

# input access key id and region
access_key_id = input("Enter the Access Key ID: ")
region = input("Enter the region: ")

# print results
s3_events = get_s3_data_events(access_key_id, region)
for event in s3_events:
    print(event)
