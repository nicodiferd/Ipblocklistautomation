import os
import requests
import json
import sys

BASE_URL    = "https://dashboard.signalsciences.net/api/v0"
SIGSCI_HEADERS = {
      'Content-type': 'application/json',
      'x-api-user': "",
      'x-api-token': ""
   }

def getBlockList():
   GET_LIST = BASE_URL + 'Shh:)'

   response = requests.get(GET_LIST, headers=SIGSCI_HEADERS)

   response.raise_for_status()
   return "\n".join(response.json()["entries"])

def updateBlockList(additions, deletions):
   UPDATE_LIST = BASE_URL + ':)'

   params = {
      "entries": {
         "additions": [],
         "deletions": []
      }
   }
   params["entries"]["additions"] = additions
   params["entries"]["deletions"] = deletions

   print(params)
   response = requests.patch(UPDATE_LIST, headers=SIGSCI_HEADERS, json=params)
   return response

if __name__ == '__main__':
   with open('./sigsci.secrets', "r") as f:
      credentials = json.load(f)
   SIGSCI_HEADERS["x-api-user"]  = credentials["username"]
   SIGSCI_HEADERS["x-api-token"] = credentials["password"]

   if len(sys.argv) > 2:
      ip = [sys.argv[2]]
      if sys.argv[1] == "add":
         status = updateBlockList(ip, [])
      elif sys.argv[1] == "remove":
         status = updateBlockList([], ip)
      print(status)
   else:
      print(getBlockList())