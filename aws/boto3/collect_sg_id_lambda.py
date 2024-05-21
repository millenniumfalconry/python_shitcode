import json
import boto3

def lambda_handler(event, context):
    instance_id = event['instance_id']
    bad_ip_address = event['bad_ip_address']
    ec2_client = boto3.client('ec2')

    
    # Get the instance details
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    
    if not response['Reservations']:
        return "No instances found with the provided ID."
    
    instance = response['Reservations'][0]['Instances'][0]
    security_group_ids = instance['SecurityGroups']
    
    if not security_group_ids:
        return "No security groups found for the instance."
    
    security_groups = ec2_client.describe_security_groups(GroupIds=[sg['GroupId'] for sg in security_group_ids])
    
    # Prepare the response payload
    response_payload = []
    
    # Extract security group details
    for sg in security_groups['SecurityGroups']:
        security_group = {
            'SecurityGroupId': sg['GroupId'],
            'Description': sg['Description'],
            'InboundRules': []
            #'OutboundRules': []
        }
        
        # Extract inbound rules
        for rule in sg['IpPermissions']:
            inbound_rule = {
                'FromPort': rule['FromPort'],
                'ToPort': rule['ToPort'],
                'IpRanges': [ip_range['CidrIp'] for ip_range in rule['IpRanges']]
            }
            security_group['InboundRules'].append(inbound_rule)
        
    #     # Extract outbound rules
    #     for rule in sg['IpPermissionsEgress']:
    #         outbound_rule = {
    #             'FromPort': rule['FromPort'],
    #             'ToPort': rule['ToPort'],
    #             'IpRanges': [ip_range['CidrIp'] for ip_range in rule['IpRanges']]
    #         }
    #         security_group['OutboundRules'].append(outbound_rule)
        
        # Add the security group to the response payload
        response_payload.append(security_group)

        return response_payload

    # Find security group rule matching the IP address
    matching_rule = None

    for sg in security_groups:
        for rule in sg['IpPermissions']:
            for ip_range in rule.get('IpRanges', []):
                if ip_range['CidrIp'] == ip_address:
                    matching_rule = {
                        'SecurityGroupId': sg['GroupId'],
                        'FromPort': rule['FromPort'],
                        'ToPort': rule['ToPort'],
                        'IpProtocol': rule['IpProtocol'],
                        'IpRange': ip_range['CidrIp']
                    }
                    break

    return matching_rule

    # Replace 'ip_address' with the IP address you want to check access for
    ip_address = 'bad_ip_address'
    matching_rule = get_security_group_rule(ip_address)

    if matching_rule:
        print("Matching security group rule found:")
        print(f"Security Group ID: {matching_rule['SecurityGroupId']}")
        print(f"From Port: {matching_rule['FromPort']}")
        print(f"To Port: {matching_rule['ToPort']}")
        print(f"IP Protocol: {matching_rule['IpProtocol']}")
        print(f"IP Range: {matching_rule['IpRange']}")
    else:
        print("No matching security group rule found.")




###aws lambda invoke --function-name your-lambda-function-arn --payload '{"instance_id": "your-instance-id"}' output.json
