import boto3

# Known bad IP addresses
bad_ip_addresses = ["1.2.3.4", "5.6.7.8", "9.10.11.12"]

# AWS credentials and region
#aws_access_key_id = "YOUR_ACCESS_KEY"
#aws_secret_access_key = "YOUR_SECRET_KEY"
#aws_region = "us-west-1"

# WAF WebACL ID
waf_webacl_id = "YOUR_WAF_WEBACL_ID"

# Create WAF client
waf_client = boto3.client('wafv2', region_name=aws_region, aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key)

try:
    # Get current IP sets in the WebACL
    response = waf_client.list_ip_sets(Scope='REGIONAL', Limit=100, NextMarker='')
    ip_sets = response['IPSets']

    # Get the IP set ID for the WebACL
    ip_set_id = None
    for ip_set in ip_sets:
        if ip_set['Name'] == waf_webacl_id:
            ip_set_id = ip_set['Id']
            break

    if ip_set_id:
        # Update the IP set with bad IP addresses
        response = waf_client.update_ip_set(
            Name=waf_webacl_id,
            Scope='REGIONAL',
            Id=ip_set_id,
            Addresses=bad_ip_addresses,
            LockToken='IGNORED'
        )
        print("WAF IP set updated successfully!")
    else:
        print("IP set ID not found for the specified WAF WebACL ID.")
except Exception as e:
    print(f"Error updating WAF IP set: {str(e)}")
