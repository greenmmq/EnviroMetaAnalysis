# EnviroMetaAnalysis

The EnviroMetaAnalysis queries journal articles published between 2013-2023 from a subset of journals related to the field of Environmental Sciences to explore the trends in environmental research around the world. These metadata were sourced from [OpenAlex](https://openalex.org/), stored on a [MongoDB](https://mongodb.com/) server, and analyzed with Python using [Jupyter](https://jupyter.org) notebooks. 

This project is completed as part of the Indiana University FADS Summer 2023 program.

## Program Operation

The `src` folder contains a script to query journal article metadata from OpenAlex and write them into local MongoDB server as a document for each article. To save some time and start working with this dataset directly, one can undertake the following steps:

1. [Install Docker](https://docs.docker.com/get-docker/)
2. Acquire `db.tar.zst` (ask the project admin...) and extract it to `./data/db`
3. From this directory run `docker compose up`

This will create and run a Docker container running MongoDB with the queried data from OpenAlex, reachable at this URI: `mongodb://localhost:27017`.

When finished, close the container with `docker compose down`. 

## Conceptual Overview

```mermaid
flowchart TB
    
    subgraph G["Data Source"]
        oa[("OpenAlex\nAPI")]
    end

    oa--query OpenAlex--> inbound
    
    inbound[[./src/alex2mongo.py]]

    inbound--write new records-->B    
    
    compose[[./docker-compose.yml]]--create container-->B

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


