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
    # get creds securely from ignored json
    with open("security/creds.json", "rb") as f:
        creds = json.load(f)

    # connect to OpenAlex API
    pyalex.config.email = creds["email"]  # your email here
    # set mongo uri variables
    uid = creds["uid"]
    pwd = creds["pwd"]
    cluster = creds["cluster"]

    uri = f"mongodb+srv://{uid}:{pwd}@{cluster}.mongodb.net/?retryWrites=true&w=majority"

    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client["OpenAlexJournalArticles"]
    collection = database["Works"]

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to EnviroMetaAnalysis MongoDB!")
    except Exception as e:
        print(e)

    return collection


def main():

    collection = mongoConnect()

    journal_articles = pyalex.Works().filter(primary_location={"source":{"id":"S13479253"}}).get(100)
    print(f"Results length: {len(journal_articles)}\nInserting documents...")
    i=0
    for docs in journal_articles:
       for d in docs:  # iterate over key-value pairs
            print(type(BSON.encode(dict(d))))
            print(type(docs))
            print(type(journal_articles))
            collection.insert_one(d) # your collection object here
            i+=1
    print(f"Successfully inserted {i} documents!")
    

if __name__ == "__main__":
    main()

