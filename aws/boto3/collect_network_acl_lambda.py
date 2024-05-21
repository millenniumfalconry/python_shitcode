import boto3

def lambda_handler(event, context):
    # EC2 instance ID
    ec2_instance_id = "YOUR_EC2_INSTANCE_ID"

    # AWS credentials and region
    aws_access_key_id = "YOUR_ACCESS_KEY"
    aws_secret_access_key = "YOUR_SECRET_KEY"
    aws_region = "us-west-1"

    # Create EC2 client
    ec2_client = boto3.client('ec2', region_name=aws_region, aws_access_key_id=aws_access_key_id,
                              aws_secret_access_key=aws_secret_access_key)

    try:
        # Get the Network ACL associations for the EC2 instance
        response = ec2_client.describe_instances(InstanceIds=[ec2_instance_id])
        network_acl_associations = response['Reservations'][0]['Instances'][0]['NetworkAclAssociationIds']

        network_acl_ids = []
        # Get the Network ACL IDs associated with the EC2 instance
        for association_id in network_acl_associations:
            response = ec2_client.describe_network_acls(Filters=[{'Name': 'association.network-acl-association-id', 'Values': [association_id]}])
            network_acl_ids.append(response['NetworkAcls'][0]['NetworkAclId'])

        return {
            'statusCode': 200,
            'body': network_acl_ids
        }
    except Exception as e:
        return {
            'statusCode': 500,
            'body': f'Error enumerating Network ACL IDs: {str(e)}'
        }
