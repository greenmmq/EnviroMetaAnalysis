# This script ETLs data from the OpenAlex API to a MongoDB Server
# Mark Green - 7/16/23

import argparse
from datetime import datetime
import logging
import numpy as np
import pandas as pd
import pyalex
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import time
from tqdm import tqdm


def mongoConnect(uri):
    """
    This function connects to the local MongoDB server running on port 27017
    It creates, or connects to an existing, database 'OpenAlexJournals'...
    ...and collection 'works'.
    """ 
    # setup MongoDB client and collection
    client = MongoClient(uri, server_api=ServerApi('1'))
    database = client["OpenAlexJournals"]
    collection = database["works"]
    # Send a ping to confirm a successful connection
    print("Ping your deployment...")
    client.admin.command('ping')
    print("Successfully connected to MongoDB!")
    
    return client, database, collection


def alex2mongoPipe(collection,logger):
    """
    This function queries OpenAlex API and pipes the results to the MongoDB server.
    Currently requires manual reconfiguration for any new queries. 
    """
    # Select OpenAlex fields
    selections = ["title","language", "publication_year","publication_date",
                  "type","primary_location","authorships","biblio",
                  "concepts","abstract_inverted_index"]
    # read-in list of ISSNs to filter OpenAlex query
    df = pd.read_excel('../data/Journal_List_Clarivate_Scopus_V1.xlsx',header=2)[:272]
    df['ISSN'] = df['ISSN'].fillna(df['eISSN'])
    # paginate the OpenAlex query and write docs to MongoDB collection
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
            logger.info(f"#### START ERROR LOG ####\n{e}\n####  END ERROR LOG  ####")


def main():
    """
    This script makes the MongoDB connection and executes the OpenAlex query pipeline...
    ...with logging and error handling.
    """
    print("Begin alex2mongo.py...")
    # get arguments
    parser = argparse.ArgumentParser(
        prog='Alex2Mongo Pipeline',
        description='Writes OpenAlex query results to MongoDB.',
        epilog='Manually edit OpenAlex queries and MongoDB connection in script.'
    )
    uri = parser.add_argument('-u','--uri',required=True,
                              help="URI for target MongoDB server")
    email = parser.add_argument('-e','--email',required=True,
                                help="email for OpenAlex API courtesy")
    args = parser.parse_args()
    pyalex.config.email = args.email  # set email for OpenAlex API courtesy
    # setup log file
    try:  ### WARNING! this clears the log file if one already exists....
        with open("alex2mongo.log","w") as file: pass
    finally:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler('alex2mongo.log')
        logger.addHandler(handler)
    # begin logging
    logger.info('Alex2Mongo Pipeline Logs')
    logger.info(f"{datetime.now()}")
    logger.info('------------------------')
    # connect to MongoDB
    connected = False
    try:
        client, _, collection = mongoConnect(args.uri)
        connected = True
        logger.info(f'Connected to: {collection}')
        logger.info('------------------------')
    except Exception as e:
        logger.info('Connection Failure!')
        logger.info(f"#### START ERROR LOG ####\n{e}\n####  END ERROR LOG  ####")
        print("Connection failure! See alex2mongo.log for more details....")
    # execute OpenAlex query pipeline
    if connected:
        try:  ### WARNING! This can take a very long time....
            alex2mongoPipe(collection=collection,logger=logger)
            print("Successfully inserted OpenAlex documents to MongoDB!")
        except Exception as e:
            logger.info('Pipeline Failure!')
            logger.info(f"#### START ERROR LOG ####\n{e}\n####  END ERROR LOG  ####")
            print("Pipeline failure! See alex2mongo.log for more details....")
        # final logs
        logger.info('------------------------') 
        logger.info(f"{datetime.now()}")
        logger.info('Operation Complete!')
        # graceful exit
        client.close()
        print("MongoDB connection closed.")
    print('alex2mongo.py is complete!')


if __name__ == "__main__":
    main()

