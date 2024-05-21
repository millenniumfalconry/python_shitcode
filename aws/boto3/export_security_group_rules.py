import boto3

def list_security_group_rules(security_group_id):
    ec2_client = boto3.client('ec2')

    try:
        # Describe security group rules
        response = ec2_client.describe_security_group_rules(Filters=[{
            'Name': 'group-id',
            'Values': [security_group_id]
        }])
        
        if not response['SecurityGroupRules']:
            print("No security group rules found for the provided ID.")
            return

        print(f"Security Group ID: {security_group_id}")
        print("Security Group Rules:")
        for rule in response['SecurityGroupRules']:
            print(f"Rule ID: {rule['SecurityGroupRuleId']}")
            print(f"Protocol: {rule.get('Protocol', 'N/A')}")
            print(f"From Port: {rule.get('FromPort', 'N/A')}")
            print(f"To Port: {rule.get('ToPort', 'N/A')}")

            ip_ranges = rule.get('CidrIpv4Ranges', [])
            if ip_ranges:
                print("IP Ranges:")
                for ip_range in ip_ranges:
                    cidr = ip_range['CidrIpv4']
                    if cidr.endswith('/32'):  # Single IP address
                        print(f"  {cidr}")
                    else:
                        print(f"  {cidr} (CIDR block)")

            prefix_list_ids = rule.get('PrefixListIds', [])
            if prefix_list_ids:
                print("Prefix List IDs:")
                for prefix_list_id in prefix_list_ids:
                    print(f"  {prefix_list_id['PrefixListId']}")

            source_group_ids = rule.get('UserIdGroupPairs', [])
            if source_group_ids:
                print("Source Security Group IDs:")
                for source_group_id in source_group_ids:
                    print(f"  {source_group_id['GroupId']}")

            print("")

    except ec2_client.exceptions.ClientError as e:
        if e.response['Error']['Code'] == 'InvalidGroup.NotFound':
            print("Invalid security group ID provided.")
        else:
            print("An error occurred while describing security group rules.")

# Replace 'security_group_id' with the ID of your security group
security_group_id = 'sg-00000000000'

list_security_group_rules(security_group_id)
