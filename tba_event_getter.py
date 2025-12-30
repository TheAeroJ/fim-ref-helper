from datetime import date
import json
import requests
from tba_handler import get_tba_response

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
    districtHistoryResponse = get_tba_response("/district/" + regionID + "/history")
    if districtHistoryResponse is None:
        print("Could not retrieve district history; exiting.")
        exit(1)
    else:
        # Make a Python object from the JSON response
        distHistoryJson = json.loads(districtHistoryResponse.json())
    


    

# Set up a Python object to store event data in the date range
eventsDict = {}

# Figure out when districts began for the specified region


# Get events for each year prior to the introduction of the district system
for seasonYear in range(1992, 2010):
    apiString = baseApiURL + "/events/" + str(seasonYear) + "/simple"
    yearEvents = requests.get(apiString, headers=requestHeaders, params=requestParams)
    # From yearEvents, create a dictionary of events filtered 

def main():
    return