from datetime import date
from dotenv import load_dotenv
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

requestParams = ""

# Establish date at time of request
nextYear = date.today().year + 1
# Specify region type (of District, State/Province, or Country)
regionType = "district"
regionID = "fim"
stateID = "mi"
countryID = ""



# Figure out the first year the region had district system if applicable
if regionType == "district":
    # Query the TBA API to get district info

    

# Set up a Python object to store event data in the date range
eventsDict = {}

# Get events for each year prior to the introduction of the district system
for seasonYear in range(1992, 2010):
    apiString = baseApiURL + "/events/" + str(seasonYear) + "/simple"
    yearEvents = requests.get(apiString, headers=requestHeaders, params=requestParams)
    # From yearEvents, create a dictionary of events filtered 

def getDistrictHistory(districtID):
    apiString = baseApiURL + "/district/" + districtID + "/history"
    districtHistory = requests.get(apiString, headers=requestHeaders, params=requestParams)
    if districtHistory.status_code != 200:
        print("Failed to get district history for " + districtID + ", status code: " + str(districtHistory.status_code))
        return None
    try:
        historyJson = districtHistory.json()
        return historyJson
    except json.JSONDecodeError:
        print("Failed to decode JSON response for district history.")
        return None
    

def main():
    return