from dotenv import load_dotenv
import argparse
import json
import os
import requests

load_dotenv()

jfmKey = os.getenv("jfmKey")
authHead = "X-TBA-Auth-Key"

baseApiURL = "https://www.thebluealliance.com/api/v3"

requestHeaders = {
    authHead: jfmKey,
    "Accept": "application/json"
}

def main():
    return

if __name__ == "__main__":
    main()