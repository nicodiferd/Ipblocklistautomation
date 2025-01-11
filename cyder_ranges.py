from ipaddress import ip_network, ip_address

def is_ip_whitelisted(whitelist_cidrs, ip_to_check):
    # Convert the input IP to an IP address object
    ip_obj = ip_address(ip_to_check)
    
    # Iterate through each CIDR in the whitelist
    for cidr in whitelist_cidrs:
        # Convert each CIDR to an IP network object
        network = ip_network(cidr)
        # Check if the IP is within the network
        if ip_obj in network:
            return True
    
    # If the IP is not found in any of the CIDR ranges, return False
    return False

# Example usage:
whitelist = ['207.62.152.0/21', '207.62.160.0/21', '207.62.168.0/22', '198.188.150.0/23','198.188.152.0/21','129.65.0.0/16','10.151.0.0/16','192.168.40.0/21','10.145.128.0/17','172.31.0.0/20',]
ip_to_check = '207.62.160.233'
result = is_ip_whitelisted(whitelist, ip_to_check)
print(result)  # Output: True
