import boto3

def enumerate_security_groups(instance_id):
    ec2_client = boto3.client('ec2')
    
    # Get the instance details
    response = ec2_client.describe_instances(InstanceIds=[instance_id])
    
    if not response['Reservations']:
        print("No instances found with the provided ID.")
        return
    
    instance = response['Reservations'][0]['Instances'][0]
    security_group_ids = instance['SecurityGroups']
    
    if not security_group_ids:
        print("No security groups found for the instance.")
        return
    
    security_groups = ec2_client.describe_security_groups(GroupIds=[sg['GroupId'] for sg in security_group_ids])
    
    # Print security group details
    for sg in security_groups['SecurityGroups']:
        print(f"Security Group ID: {sg['GroupId']}")
        print(f"Description: {sg['Description']}")
        #print("Inbound Rules:")
        #for rule in sg['IpPermissions']:
        #    print(f"- From port {rule['FromPort']} to port {rule['ToPort']}")
        #    for ip_range in rule['IpRanges']:
        #        print(f"  - IP Range: {ip_range['CidrIp']}")
        #print("Outbound Rules:")
        #for rule in sg['IpPermissionsEgress']:
        #    print(f"- From port {rule['FromPort']} to port {rule['ToPort']}")
        #    for ip_range in rule['IpRanges']:
        #        print(f"  - IP Range: {ip_range['CidrIp']}")
        #print("------------------------")

# Replace 'instance_id' with the actual ID of your EC2 instance
instance_id = 'i-0561dc1d5a003dd67'
enumerate_security_groups(instance_id)
