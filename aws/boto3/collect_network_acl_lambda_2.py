import boto3

def lambda_handler(event, context):
    # EC2 instance ID
    ec2_instance_id = "YOUR_EC2_INSTANCE_ID"

    # Create EC2 client
    ec2_client = boto3.client('ec2')

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

        return {
            'statusCode': 200,
            'body': {
                'subnetId': subnet_id,
                'vpcId': vpc_id,
                'networkAclIds': network_acl_ids
            }
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error enumerating Subnet, VPC, and Network ACL IDs: {str(e)}'
        }
