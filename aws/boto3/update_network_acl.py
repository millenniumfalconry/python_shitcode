import boto3

def lambda_handler(event, context):
    # Known bad IP addresses
    bad_ip_addresses = ["1.2.3.4", "5.6.7.8", "9.10.11.12"]

    # AWS credentials and region
    #aws_access_key_id = "YOUR_ACCESS_KEY"
    #aws_secret_access_key = "YOUR_SECRET_KEY"
    #aws_region = "us-west-1"

    # Network ACL ID
    network_acl_id = "YOUR_NETWORK_ACL_ID"

    # Create EC2 client
    ec2_client = boto3.client('ec2', region_name=aws_region, aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)

    try:
        # Get current entries in the Network ACL
        response = ec2_client.describe_network_acls(NetworkAclIds=[network_acl_id])
        entries = response['NetworkAcls'][0]['Entries']

        # Remove existing entries for bad IP addresses
        for ip_address in bad_ip_addresses:
            for entry in entries:
                if entry['CidrBlock'] == f"{ip_address}/32":
                    ec2_client.delete_network_acl_entry(NetworkAclId=network_acl_id, RuleNumber=entry['RuleNumber'])
                    print(f"Removed entry for IP address: {ip_address}")

        # Add new entries for bad IP addresses
        rule_number = 100
        for ip_address in bad_ip_addresses:
            ec2_client.create_network_acl_entry(NetworkAclId=network_acl_id,
                                                RuleNumber=rule_number,
                                                Protocol='-1',
                                                RuleAction='deny',
                                                Egress=False,
                                                CidrBlock=f"{ip_address}/32")
            rule_number += 100
            print(f"Added entry for IP address: {ip_address}")

        return {
            'statusCode': 200,
            'body': 'Network ACL updated successfully!'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error updating Network ACL: {str(e)}'
        }
