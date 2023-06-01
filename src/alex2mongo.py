# This script ETLs data from the OpenAlex API to a MongoDB Server
# TESTING
# Mark Green - 5/23/23

#import pymongo
import pyalex
from pprint import pprint

pyalex.config.email = "margree@iu.edu"  # your email here



def main():
    result = pyalex.Works() \
        .filter(institutions={"is_global_south":True}) \
        .filter(primary_location={"source":{"id":"S13479253"}}) \
        .group_by("institutions.country_code") \
        .get()

    pprint(result)
 

if __name__ == "__main__":
    main()

