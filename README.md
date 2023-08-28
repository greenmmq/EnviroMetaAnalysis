# EnviroMetaAnalysis

The EnviroMetaAnalysis study queries journal articles published between 2013-2023 from a subset of journals related to the *Environmental Science* to explore the trends in environmental research around the world. These metadata were gathered from [OpenAlex](https://openalex.org/), stored on a [MongoDB](https://mongodb.com/) server, and analyzed with Python using [Jupyter](https://jupyter.org) notebooks. 

This project is designed to support the [International Panel on Chemical Pollution](https://www.ipcp.ch/activities/ipcp-white-paper-on-the-scope-and-functions-of-the-future-science-policy-panel), established as part of United Nations Environment Assembly resolution 5/8. This work is completed through the Indiana University FADS Summer 2023 program for the Luddy School of Informatics, Computing, and Engineering.

## Program Operation

The `src` folder contains a script, `alex2mongo.py`, to query journal article metadata from OpenAlex and write them into local MongoDB server as a document for each article. To save some time and start working with this dataset directly, one can undertake the following steps:

1. Install [Docker](https://docs.docker.com/get-docker/)
2. Acquire `db.tar.gz` from project admin and save it to the `./data/` directory
3. From the `./data/` directory run the following command to extract the MongoDB database files: 
```shell
tar xzf db.tar.gz db
```
4. Build the container with the following command from this root `EnviroMetaAnalysis` directory: 

```shell
docker run -d --name mongodb_fads \
  -v <absolute-path-to-repo>/EnviroMetaAnalysis/data/db:/data/db \
  -p 27017:27017 mongo:latest
```

This will create and run a Docker container running `MongoDB` with the queried data from OpenAlex. The data is reachable at this URI: `mongodb://localhost:27017`, in the `journals` collection of the `OpenAlexEnvironmental` database. 

## Conceptual Overview

```mermaid
flowchart TB
    
    subgraph G["Data Source"]
        oa[("OpenAlex\nAPI")]
    end

    oa--query OpenAlex--> inbound
    
    inbound[[./src/alex2mongo.py]]

    inbound--write new records-->B    
    
    compose[docker run]--create container-->B

    subgraph B["Docker Container"]
        mongo[("Mongo Server\nlocalhost:27017")]
        volume(["MongoDB Volume\n./data/db"])
        volume<-->mongo
    end
    
    B--query MongoDB-->C;

    subgraph C["Visualizations"]
        stats(("Statistics\nWordCloud\nPlots and Graphs"))
    end
```


