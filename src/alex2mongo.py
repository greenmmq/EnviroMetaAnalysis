# This script ETLs data from the OpenAlex API to a MongoDB Server
# TESTING
# Mark Green - 5/23/23

import json
from bson import BSON
from pprint import pprint
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pyalex

def mongoConnect():
    """
    This function connects to the MongoDB server using secure credentials
    """

    with open("security/creds.json", "rb") as f:
        creds = json.load(f)  # creds from ignored json - ask admin for one...

    pyalex.config.email = creds["email"]
    uid = creds["uid"]
    pwd = creds["pwd"]
    cluster = creds["cluster"]

    uri = f"mongodb+srv://{uid}:{pwd}@{cluster}.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client["OpenAlexJournalArticles"]
    collection = database["Works"]


    try:  # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Pinged your deployment...\nSuccessfully connected to EnviroMetaAnalysis MongoDB!")
    except Exception as e:
        print(e)

    return client, database, collection


def alex2mongoPipe(collection):
    """
    This function queries OpenAlex API and pipes the results to the MongoDB server
    """

    print("Querying OpenAlex API...")

    # use PyAlex library to write desired query q    
    # oa paging: https://pypi.org/project/pyalex/
    # Example query to get first page (25 works) from Env Sci Tech Journal:
    # query = pyalex.Works().filter(primary_location={"source":{"id":"S13479253"}})
    # ENTER QUERY BELOW...
    query = pyalex.Works().filter(primary_location={"source":{"id":"S13479253"}}) \
                          .paginate(per_page=200, n_max=10000)

    #print(f"Results length: {len(query)})
    print("Inserting documents...")
    i=0
    for page in query:
        for doc in page:
            d = dict(doc)
            collection.insert_one(d)
            i+=1
    print(f"Successfully inserted {i} documents!")


def main():

    client, _, collection = mongoConnect()

    try:
        alex2mongoPipe(collection=collection)
    except Exception as e:
        print(e)

    client.close()

if __name__ == "__main__":
    main()

