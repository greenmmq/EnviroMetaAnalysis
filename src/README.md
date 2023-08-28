# OpenAlex to MongoDB Pipeline

Source Code for EnviroMetaAnalysis. `alex2mongo.py` can be executed by following these instructions:

1. Install [Poetry](https://python-poetry.org/docs/)
2. From this directory path, run the following command to install python dependencies and setup virtual environment
```shell
poetry install & poetry shell
```
3. Run pipeline to query OpenAlex API data and load to local `MongoDB` server: 
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

`test.py` counts the documents in the `journals` collection of `OpenAlexEnvironmental` database.

# EnviroMetaAnalysis Jupyter Notebook EDA

The EnviroMetaAnalysis jupyter notebook can be run to analyze the distribution of citation metrics across countries and income groups for a sampling of articles pertaining to a specified topic. When this notebook is run, it writes plots and `.gexf` files to the `plots` and `gephi` directories. Although it is a good step forward in this study, some more work can be done to improve the full picture. 

1. The `dev/Normalization patterns.ipynb` should be cleaned up, annotated, and elevated to the `src` directory. The plots here are precursor to the `EnviroMetaAnalysis.ipynb` and are relevant to why this particular pattern of normalization was chosen. 
2. Outputs should be refined, and run for more scenarios of interest to the core team. Improvements and tweaks should be made after further review. 
