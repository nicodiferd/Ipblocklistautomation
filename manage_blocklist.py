import requests
import os
import json, sys

BASE_URL = ":)"
SIGSCI_HEADERS = {
    'Content-type': 'application/json',
    'x-api-user': "",
    'x-api-token': ""
}

def getBlockList():
    GET_LIST = BASE_URL + ':)'
    response = requests.get(GET_LIST, headers=SIGSCI_HEADERS)
    response.raise_for_status()
    return "\n".join(response.json()["entries"])

def updateBlockList(additions, deletions):
    UPDATE_LIST = BASE_URL + ':)'
    params = {
        "entries": {
            "additions": additions,
            "deletions": deletions
        }
    }
    response = requests.patch(UPDATE_LIST, headers=SIGSCI_HEADERS, json=params)
    response.raise_for_status()
    return response

def readBlockListFile():
    with open('blocklist.txt', 'r') as file:
        return [line.strip() for line in file if line.strip()]

if __name__ == '__main__':
    with open('./sigsci.secrets', "r") as f:
        credentials = json.load(f)
    SIGSCI_HEADERS["x-api-user"] = credentials["username"]
    SIGSCI_HEADERS["x-api-token"] = credentials["password"]

    if len(sys.argv) == 2 and sys.argv[1] == "sync":
        current_block_list = getBlockList().split("\n")
        new_block_list = readBlockListFile()
        
        additions = list(set(new_block_list) - set(current_block_list))
        deletions = list(set(current_block_list) - set(new_block_list))
        
        if additions or deletions:
            status = updateBlockList(additions, deletions)
            print("Block list updated:", status.json())
        else:
            print("No changes to the block list.")
    else:
        print("Usage: python manage_blocklist.py sync")