import boto3

# EC2 instance ID
ec2_instance_id = "i-0000000000"

# AWS credentials and region
#aws_access_key_id = "YOUR_ACCESS_KEY"
#aws_secret_access_key = "YOUR_SECRET_KEY"
#aws_region = "us-west-1"

# Create EC2 client
ec2_client = boto3.client('ec2')
    #, region_name=aws_region, aws_access_key_id=aws_access_key_id,
                          #aws_secret_access_key=aws_secret_access_key)

try:
    # Get the EC2 instance details
    response = ec2_client.describe_instances(InstanceIds=[ec2_instance_id])
    instance = response['Reservations'][0]['Instances'][0]

    # Get the Subnet ID
    subnet_id = instance['SubnetId']

    # Get the VPC ID
    vpc_id = instance['VpcId']

    # Get the Network ACL associations for the Subnet
    response = ec2_client.describe_network_acls(Filters=[{'Name': 'association.subnet-id', 'Values': [subnet_id]}])
    network_acl_ids = [nacl['NetworkAclId'] for nacl in response['NetworkAcls']]

    print(f"Subnet ID: {subnet_id}")
    print(f"VPC ID: {vpc_id}")
    print("Network ACL IDs associated with the Subnet:")
    for acl_id in network_acl_ids:
        print(acl_id)
except Exception as e:
    print(f"Error enumerating Subnet, VPC, and Network ACL IDs: {str(e)}")
