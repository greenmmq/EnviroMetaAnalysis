# This script ETLs data from the OpenAlex API to a MongoDB Server
# TESTING
# Mark Green - 5/23/23

import json
from pprint import pprint
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pyalex

def mongoConnect():
    # get creds securely from ignored json
    with open("security/creds.json", "rb") as f:
        creds = json.load(f)

    # connect to OpenAlex API
    pyalex.config.email = creds[0]  # your email here
    # set mongo uri variables
    uid = creds[1]
    pwd = creds[2]
    cluster = creds[3]

    uri = f"mongodb+srv://{uid}:{pwd}@{cluster}.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to EnviroMetaAnalysis MongoDB!")
    except Exception as e:
        print(e)


def main():
    result = pyalex.Works() \
        .filter(institutions={"is_global_south":True}) \
        .filter(primary_location={"source":{"id":"S13479253"}}) \
        .group_by("institutions.country_code") \
        .get()

    pprint(result)
 

if __name__ == "__main__":
    main()

