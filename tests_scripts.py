import json

def check_ip_against_whitelist(ip):
    try:
        # Define the search_results dictionary (previously from a response)
        search_results = {
            "ip": [
                "207.62.152.0/21",
                "207.62.160.0/21",
                "207.62.168.0/22",
                "198.188.150.0/23",
                "198.188.152.0/21",
                "129.65.0.0/16",
                "10.151.0.0/16",
                "192.168.40.0/21",
                "10.145.128.0/17",
                "172.31.0.0/20",
                "169.254.*"
            ]
        }

        # Check if the IP is in the whitelist
        is_whitelisted = ip in search_results['ip']

        # Prepare the output
        outputs = {
            'is_whitelisted': is_whitelisted,
            'ip': ip
        }

        # Ensure the output is JSON-serializable
        json.dumps(outputs)  # This will raise an exception if the `outputs` object is not JSON-serializable

        # Return the results
        return outputs

    except Exception as e:
        # Handle any errors
        print(f"An error occurred: {e}")
        return {
            'is_whitelisted': False,
            'ip': ip,
            'error': str(e)
        }

# Main function to execute the script
if __name__ == "__main__":
    ip_to_check = "207.62.160.27"  # Replace with the IP you want to check
    result = check_ip_against_whitelist(ip_to_check)
    print(result)