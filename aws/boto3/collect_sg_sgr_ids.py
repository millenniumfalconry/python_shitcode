import boto3

def find_security_group_with_bad_ip(instance_id, bad_ip_address):
    ec2_client = boto3.client('ec2')

    # Describe instances
    response = ec2_client.describe_instances(InstanceIds=[instance_id])

    if not response['Reservations']:
        print("No instances found with the provided ID.")
        return

    instance = response['Reservations'][0]['Instances'][0]
    security_groups = instance.get('SecurityGroups', [])

    if not security_groups:
        print("No security groups found for the instance.")
        return

    matching_security_groups = []

    # Check security groups for bad IP address
    for sg in security_groups:
        security_group_id = sg['GroupId']
        security_group_rules = ec2_client.describe_security_group_rules(
            Filters=[{
                'Name': 'group-id',
                'Values': [security_group_id]
            }]
        )['SecurityGroupRules']

        for rule in security_group_rules:
            ip_ranges = rule.get('CidrIpv4Ranges', [])

            for ip_range in ip_ranges:
                if ip_range['CidrIpv4'] == bad_ip_address:
                    matching_security_groups.append({
                        'SecurityGroupId': security_group_id,
                        'SecurityGroupRuleId': rule['SecurityGroupRuleId']
                    })
                    break

    return matching_security_groups

# Replace 'instance_id' with the ID of your EC2 instance
instance_id = 'i-0475d38fc2fd4efe1'
# Replace 'bad_ip_address' with the specific IP address that you consider as bad
bad_ip_address = '24.34.53.12/32'

matching_security_groups = find_security_group_with_bad_ip(instance_id, bad_ip_address)

if matching_security_groups:
    print("Matching security groups:")
    for sg in matching_security_groups:
        print(f"Security Group ID: {sg['SecurityGroupId']}")
        print(f"Security Group Rule ID: {sg['SecurityGroupRuleId']}")
else:
    print("No matching security groups found.")
