from dotenv import load_dotenv
import argparse
import json
import os
import requests

def get_tba_response(suffix):
    load_dotenv()

    jfmKey = os.getenv("jfmKey")
    authHead = "X-TBA-Auth-Key"

    baseApiURL = "https://www.thebluealliance.com/api/v3"

    requestHeaders = {
        authHead: jfmKey,
        "Accept": "application/json"
    }

    apiString = baseApiURL + suffix
    response = requests.get(apiString, headers=requestHeaders)
    if response.status_code != 200:
        print("Failed to get TBA response for suffix " + suffix + ", status code: " + str(response.status_code))
        return None
    else:
        print("Successfully received TBA response for suffix " + suffix)
        return response
    

if __name__ == "__get_tba_response__":
    parser = argparse.ArgumentParser(description="TBA Event Getter Script")
    parser.add_argument('--suffix', type=str, help='API suffix string to be appended to base URL', required=True, default='/status')
    args = parser.parse_args()
    main(args.suffix)
