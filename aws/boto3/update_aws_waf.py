import boto3

def lambda_handler(event, context):
    # Known bad IP addresses
    bad_ip_addresses = ["1.2.3.4", "5.6.7.8", "9.10.11.12"]

    # AWS credentials and region
    #aws_access_key_id = "YOUR_ACCESS_KEY"
    #aws_secret_access_key = "YOUR_SECRET_KEY"
    #aws_region = "us-west-1"

    # Create AWS WAF client
    waf_client = boto3.client('waf')
    #, region_name=aws_region, aws_access_key_id=aws_access_key_id,
                              #aws_secret_access_key=aws_secret_access_key)

    # Web ACL ID
    web_acl_id = "YOUR_WEB_ACL_ID"

    try:
        # Get current IP sets in the Web ACL
        response = waf_client.list_ip_sets(NextMarker='', Limit=100, Scope='CLOUDFRONT', WebACLId=web_acl_id)
        ip_sets = response['IPSets']

        # Get the IP set that we want to update
        ip_set = next((x for x in ip_sets if x['Name'] == 'BadIPSet'), None)

        if ip_set:
            # Update IP set with bad IP addresses
            waf_client.update_ip_set(IPSetId=ip_set['IPSetId'], ChangeToken=ip_set['ChangeToken'],
                                     Updates=[{'Action': 'INSERT', 'IPSetDescriptor': {'Type': 'IPV4', 'Value': ip}} for ip in bad_ip_addresses])
            print("Updated WAF IP set with bad IP addresses")
        else:
            print("IP set 'BadIPSet' not found in the Web ACL")

        return {
            'statusCode': 200,
            'body': 'WAF IP set updated successfully!'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error updating WAF IP set: {str(e)}'
        }
