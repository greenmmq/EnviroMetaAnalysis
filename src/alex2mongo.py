# This script ETLs data from the OpenAlex API to a MongoDB Server
# TESTING
# Mark Green - 5/23/23

#!pip install pymongo pyalex

import json
from bson import BSON
from pprint import pprint
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pyalex
import pandas as pd
import numpy as np
from tqdm import tqdm

def mongoConnect():
    """
    This function connects to the MongoDB server using secure credentials
    """

#     with open("security/creds.json", "rb") as f:
#         creds = json.load(f)  # creds from ignored json - ask admin for one...

#     pyalex.config.email = creds["email"]
#     uid = creds["uid"]
#     pwd = creds["pwd"]
#     cluster = creds["cluster"]

    # uri = f"mongodb+srv://{uid}:{pwd}@{cluster}.mongodb.net/?retryWrites=true&w=majority"

    uri = "mongodb://localhost:27017"
    
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client["OpenAlexJournals"]
    collection = database["test"]

    try:  # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Pinged your deployment...")
        print("Successfully connected to EnviroMetaAnalysis MongoDB!")
    except Exception as e:
        print(e)

    return client, database, collection


def alex2mongoPipe(collection):
    """
    This function queries OpenAlex API and pipes the results to the MongoDB server
    """
    
    selections = ["title","language", "publication_year","publication_date",
                  "type","primary_location","authorships","biblio",
                  "concepts","abstract_inverted_index"]
    
    df = pd.read_excel('../data/Journal_List_Clarivate_mv.xlsx',header=2,)[:272]
    df['ISSN'] = df['ISSN'].fillna(df['eISSN'])
    
    print("Querying OpenAlex API and loading to MongoDB...")
    
    pyalex.config.email="margree@iu.edu"
    
    for i in tqdm(range(df.shape[0])):
        issn = df['ISSN'][i]
        query = pyalex.Works().filter(primary_location={"source":{"issn":issn}}) \
                              .filter(publication_year='>2012').select(selections) \
                              .paginate(per_page=200, n_max=None)

        for page in query:
            for doc in page:
                d = dict(doc)
                collection.insert_one(d)
        
    print("Successfully inserted OpenAlex documents to MongoDB!")
    

def main():

    client, _, collection = mongoConnect()

    try:
        alex2mongoPipe(collection=collection)
    except Exception as e:
        print(e)

    client.close()

if __name__ == "__main__":
    main()

