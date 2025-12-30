from dotenv import load_dotenv
import argparse
import json
import os
import requests

# Parse arguments

def main():
    load_dotenv()

    jfmKey = os.getenv("jfmKey")
    authHead = "X-TBA-Auth-Key"

    baseApiURL = "https://www.thebluealliance.com/api/v3"

    requestHeaders = {
        authHead: jfmKey,
        "Accept": "application/json"
    }

def scriptConfig():
    # Add arguments as needed
    return parser.parse_args()
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TBA Event Getter Script")
    parser.add_argument('--suffix', type=str, help='API suffix string to be appended to base URL', required=True, default='/status')
    args = parser.parse_args()
    main(args.suffix)
