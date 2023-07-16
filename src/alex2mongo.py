# This script ETLs data from the OpenAlex API to a MongoDB Server
# TESTING
# Mark Green - 7/16/23

from datetime import datetime
import json
import logging
import numpy as np
import pandas as pd
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pyalex
import time
from tqdm import tqdm


def mongoConnect():
    """
    This function connects to the MongoDB server using secure credentials
    """
    
    uri = "mongodb://localhost:27017"
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client["OpenAlexJournals"]
    collection = database["works"]

    try:  # Send a ping to confirm a successful connection
        client.admin.command('ping')
        print("Pinged your deployment...")
        print("Successfully connected to EnviroMetaAnalysis MongoDB!")
    except Exception as e:
        print(e)

    return client, database, collection


def alex2mongoPipe(collection,logger):
    """
    This function queries OpenAlex API and pipes the results to the MongoDB server
    """
    
    selections = ["title","language", "publication_year","publication_date",
                  "type","primary_location","authorships","biblio",
                  "concepts","abstract_inverted_index"]
    
    df = pd.read_excel('../data/Journal_List_Clarivate_mv.xlsx',header=2,)[:272]
    df['ISSN'] = df['ISSN'].fillna(df['eISSN'])
    
    print("Querying OpenAlex API and loading to MongoDB...")
    
    for i in tqdm(range(df.shape[0])):
        issn = df['ISSN'][i]
        try: 
            toc = time.perf_counter()
            query = pyalex.Works().filter(primary_location={"source":{"issn":issn}}) \
                                  .filter(publication_year='>2012').select(selections) \
                                  .paginate(per_page=200, n_max=None)     
            doc_count = 0
            for page in query:
                for doc in page:
                    d = dict(doc)
                    collection.insert_one(d)
                    doc_count += 1
            tic = time.perf_counter()
            duration = round(tic-toc,2)
            logger.info(f"{issn} :: {doc_count} articles :: {duration} seconds")
        except Exception as e:
            logger.info(f"{issn} :: Failed to load articles....")
            logger.info(f"##### START ERROR LOG #####\n{e}\n#####  END ERROR LOG  #####")

    print("Successfully inserted OpenAlex documents to MongoDB!")
    

def main():
    
    pyalex.config.email = "margree@iu.edu"
    
    try:  # clear the log file
        with open("alex2mongo.log","w") as file:
            pass
    finally:
        pass

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler('alex2mongo.log')
    logger.addHandler(handler)
    logger.info('Alex2Mongo Pipeline Logs')
    logger.info(f"{datetime.now()}")
    logger.info('------------------------')

    client, _, collection = mongoConnect()

    try:
        alex2mongoPipe(collection=collection,logger=logger)
    except Exception as e:
        print(e)

    client.close()

if __name__ == "__main__":
    main()

