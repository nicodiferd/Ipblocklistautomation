from ipaddress import ip_network, ip_address
import re

def convert_allow_list(allow_list_str):
    # Split the allow list string by '|'
    cidr_list = allow_list_str.split('|')
    converted_list = []

    for cidr in cidr_list:
        # Replace '*' with '0/24' for /8 networks, '0/16' for /16 networks, etc.
        if '*' in cidr:
            if cidr.count('.') == 3:
                cidr = cidr.replace('*', '0/24')  # Assumes it's in the format x.x.x.*
            elif cidr.count('.') == 2:
                cidr = cidr.replace('*', '0/16')  # Assumes it's in the format x.x.*.*
            elif cidr.count('.') == 1:
                cidr = cidr.replace('*', '0/8')   # Assumes it's in the format x.*.*.*
            else:
                print(f"Unrecognized CIDR format: {cidr}")
                continue
        
        # Append each CIDR with quotes around it
        converted_list.append(cidr)

    return converted_list

def check_ip_whitelist(action, success, container, results, handle, filtered_artifacts, filtered_results, custom_function, **kwargs):
    # Fetch the IP address to check from the parameters or artifacts
    ip_to_check = kwargs.get('ip')
    
    # Fetch the allow list of CIDR ranges from the parameters or artifacts
    allow_list_str = kwargs.get('Allow_List', '')

    # Convert the allow list into a list of CIDR strings
    allow_list = convert_allow_list(allow_list_str)

    # Validate that the IP is provided
    if not ip_to_check:
        print("No IP address provided to check.")
        return False

    # Convert the input IP to an IP address object
    try:
        ip_obj = ip_address(ip_to_check)
    except ValueError as e:
        print(f"Invalid IP address: {ip_to_check}. Error: {str(e)}")
        return False

    # Check if the IP is in any of the CIDR ranges in the allow list
    for cidr in allow_list:
        try:
            network = ip_network(cidr)
            if ip_obj in network:
                print(f"IP {ip_to_check} is in CIDR range {cidr}")
                return True
        except ValueError as e:
            print(f"Invalid CIDR: {cidr}. Error: {str(e)}")
            continue

    # If the IP is not found in any of the CIDR ranges
    print(f"IP {ip_to_check} is NOT in any allow list CIDR range")
    return False