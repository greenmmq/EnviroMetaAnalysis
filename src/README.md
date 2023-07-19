# OpenAlex to MongoDB Pipeline

Source Code for EnviroMetaAnalysis. `alex2mongo.py` can be executed by following these instructions:

1. Install [Poetry](https://python-poetry.org/docs/)
2. From this directory path, run the following command to install python dependencies and setup virtual environment
```shell
poetry install & poetry shell
```
3. Run pipeline to query OpenAlex API data and load to local MongoDB: 
```shell
poetry run python alex2mongo.py -u mongodb://localhost:27017 -e <your-email-here>
```

Running `alex2mongo.py --help` will provide an argument overview. Progress and errors are tracked in the log file - example provided here. 

**WARNING**

This script can take a long time to run! This particular pipeline takes >130 minutes to run.

## Testing

To test that the container is operating as expected, run the following command from this `./src/` directory: 
```shell
poetry run python test/test.py
```
