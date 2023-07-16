# OpenAlex to MongoDB Pipeline

Source Code for EnviroMetaAnalysis. `alex2mongo.py` can be executed by following these instructions:

1. Install [Poetry](https://python-poetry.org/docs/)
2. From this directory path, run command `poetry install & poetry shell` to install python dependencies and setup virtual environment. 
3. run pipeline: `poetry run python alex2mongo.py -u mongodb://localhost:27017 -e <your-email-here>`

Running `alex2mongo.py --help` will provide an argument overview. Progress and errors are tracked in the log file - an example log file is provided here. 

## **WARNING**

This script can take a long time to run! This particular pipeline takes ~130 minutes to run.

