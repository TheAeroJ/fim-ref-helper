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

# Set up a Python object to store event data in the date range
eventsDict = {}

# Get events for each year prior to the introduction of the district system
for seasonYear in range(1992, 2010):
    apiString = baseApiURL + "/events/" + str(seasonYear) + "/simple"
    yearEvents = requests.get(apiString, headers=requestHeaders, params=requestParams)
    # From yearEvents, create a dictionary of events filtered 

