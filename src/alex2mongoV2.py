#!/usr/bin/env python
# coding: utf-8

# In[70]:


import json
#from bson import BSON
from pprint import pprint
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pyalex
import pandas as pd
import numpy as np
from tqdm import tqdm


# In[79]:


query = pyalex.Works().filter(primary_location={"source":{"issn":"2198-6592"}})                        .filter(publication_year='>2012').select(["title", "publication_year","publication_date",
                                                                "type","primary_location","authorships","biblio",
                                                                 "concepts","abstract_inverted_index"]) \
                       .paginate(per_page=200, n_max=None)


# In[42]:


df = pd.read_excel('Journal_List_Clarivate_mv.xlsx',header=2,)
df = df[:272]
df.head()


# In[56]:


df['ISSN'] = df['ISSN'].fillna(df['eISSN'])


# In[61]:


cluster = MongoClient("mongodb+srv://jerithom:Jerin1107@jerithom.gntipua.mongodb.net/")
db = cluster["globalsouth"]
collection = db["journals"]


# In[83]:


for i in tqdm(range(df.shape[0])):
    issn = df['ISSN'][i]
    query = pyalex.Works().filter(primary_location={"source":{"issn":issn}})                        .filter(publication_year='>2012').select(["title","language", "publication_year","publication_date",
                                                                "type","primary_location","authorships","biblio",
                                                                 "concepts","abstract_inverted_index"]) \
                       .paginate(per_page=200, n_max=None)
    for page in query:
        for doc in page:
            d = dict(doc)
            collection.insert_one(d)


# In[ ]:




