import phantom.rules as phantom
import json

def ipToInt(ip):
    o = list(map(int, ip.split('.')))
    res = (16777216 * o[0]) + (65536 * o[1]) + (256 * o[2]) + o[3]
    return res

def isIpInSubnet(ip, ipNetwork, maskLength):
    ipInt = ipToInt(ip)
    ipNetworkInt = ipToInt(ipNetwork)

    subnetMask = (0xFFFFFFFF << (32 - maskLength)) & 0xFFFFFFFF

    networkAddress = ipNetworkInt & subnetMask
    broadcastAddress = networkAddress | ~subnetMask & 0xFFFFFFFF

    return networkAddress <= ipInt <= broadcastAddress

def custom_function(container=None, handle=None, **kwargs):
    """
    This function checks if an IP is within a given subnet.
    
    Args:
        container (dict): The container dictionary.
        handle (dict): The handle dictionary.
    
    Returns:
        dict: The result containing success status and boolean result.
    """
    
    # Extract parameters
    parameters = phantom.collect2(container=container, datapath=['ip', 'ip_network', 'mask_length'])
    
    ip = parameters[0][0]
    ip_network = parameters[0][1]
    mask_length = int(parameters[0][2])
    
    # Check if IP is in the subnet
    result = isIpInSubnet(ip, ip_network, mask_length)
    
    # Create output
    outputs = {
        'is_ip_in_subnet': result
    }
    
    # Return result
    return outputs