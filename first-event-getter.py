from dotenv import load_dotenv
import base64
import json
import os
import requests

# Set up authorization
load_dotenv()
jmtoken = os.getenv("jmtoken")
jmusername = os.getenv("jmusername")

jmAuthString = jmusername + ":" + jmtoken
jmAuthBytes = jmAuthString.encode('ascii')
jmAuthBase64Bytes = base64.b64encode(jmAuthBytes)
authString = jmAuthBase64Bytes.decode('ascii')

# Test the connection to the API
# TODO: Implement some logic to handle failed connections and quit gracefully
r = requests.get('https://frc-api.firstinspires.org/v3.0/2025', headers={'Authorization': 'Basic ' + authString})
print("Status Code: " + r.status_code.__str__())
print("Headers: " + str(r.headers))
print("JSON Response: " + r.json().__str__())

# Set up a Python object to store event data in the date range


for seasonYear in range (2025, 2027):
    # Do things here
    apiString = 'https://frc-api.firstinspires.org/v3.0/' + str(seasonYear) + '/events?districtCode=FIM'
    yearEvents = requests.get(apiString, headers={'Authorization': 'Basic ' + authString, 'Accept': 'application/json'})
    
    print("Status Code: " + yearEvents.status_code.__str__() + " " + yearEvents.reason)
    print("Headers: " + str(yearEvents.headers))


    
    print(str(seasonYear) + " Events: ")
    try:
        eventsJson = yearEvents.json()["Events"]
        print("Received a JSON response")
        print(json.dumps(eventsJson, indent=4))
    except json.JSONDecodeError:
        print("Failed to decode JSON response.")
        try:
            eventsText = yearEvents.text
            print("Received a plaintext response")
            # print(eventsText)
        except Exception as e:
            print("Failed to get text response: " + str(e))
            break