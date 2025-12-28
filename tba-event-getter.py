from dotenv import load_dotenv
import json
import os
import requests

load_dotenv()

jfmKey = os.getenv("jfmKey")
authHead = "X-TBA-Auth-Key"

tba = ""

requests.request("GET", )
