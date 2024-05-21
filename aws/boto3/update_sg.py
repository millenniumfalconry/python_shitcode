import boto3

def lambda_handler(event, context):
    # Known bad IP addresses
    bad_ip_addresses = ["1.2.3.4", "5.6.7.8", "9.10.11.12"]

    # AWS credentials and region
    # aws_access_key_id = "YOUR_ACCESS_KEY"
    # aws_secret_access_key = "YOUR_SECRET_KEY"
    # aws_region = "us-west-1"

    # Create EC2 client
    ec2_client = boto3.client('ec2', region_name=aws_region, aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)

    # Security Group ID
    security_group_id = "YOUR_SECURITY_GROUP_ID"

    try:
        # Get current IP permissions for the security group
        response = ec2_client.describe_security_groups(GroupIds=[security_group_id])
        ip_permissions = response['SecurityGroups'][0]['IpPermissions']

        # Revoke existing ingress rules for bad IP addresses
        for ip_address in bad_ip_addresses:
            revoke_permissions = []
            for permission in ip_permissions:
                for ip_range in permission.get('IpRanges', []):
                    if ip_range['CidrIp'] == f"{ip_address}/32":
                        revoke_permissions.append({
                            'IpProtocol': permission['IpProtocol'],
                            'FromPort': permission.get('FromPort'),
                            'ToPort': permission.get('ToPort'),
                            'IpRanges': [{'CidrIp': ip_range['CidrIp'], 'Description': ip_range.get('Description')}]
                        })
            if revoke_permissions:
                ec2_client.revoke_security_group_ingress(GroupId=security_group_id, IpPermissions=revoke_permissions)
                print(f"Revoked ingress rules for IP address: {ip_address}")

        # Add new ingress rules for bad IP addresses
        for ip_address in bad_ip_addresses:
            ec2_client.authorize_security_group_ingress(GroupId=security_group_id,
                                                        IpPermissions=[
                                                            {
                                                                'IpProtocol': '-1',
                                                                'FromPort': -1,
                                                                'ToPort': -1,
                                                                'IpRanges': [
                                                                    {
                                                                        'CidrIp': f"{ip_address}/32",
                                                                        'Description': 'Bad IP'
                                                                    },
                                                                ],
                                                            },
                                                        ])
            print(f"Added ingress rule for IP address: {ip_address}")

        return {
            'statusCode': 200,
            'body': 'Security group updated successfully!'
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error updating security group: {str(e)}'
        }


###Test event
#{
#  "bad_ip_addressses": "1.1.1.1"
#  "security_group_id": "i-00000000000"
#}
