import os
import sys
from dotenv import load_dotenv
import json
import certifi
import pandas as pd
import pymongo
from networksecurity.logging import logger
from networksecurity.exception.exception import NetworkSecurityException

# Load environment variables
load_dotenv()
MONGODB_URL = os.getenv("MONGO_DB_URL")

if not MONGODB_URL:
    raise ValueError("MONGO_DB_URL is not defined in the environment variables.")

# Certifi for HTTPS connections
ca = certifi.where()

class NetworkDataExtract:
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json(self, file_path):
        try:
            # Check if file exists
            if not os.path.exists(file_path):
                raise FileNotFoundError(f"The file {file_path} does not exist.")
            
            # Read CSV and convert to JSON
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def insert_to_mongodb(self, collection, database, records):
        try:
            # Initialize MongoDB client
            mongo_client = pymongo.MongoClient(MONGODB_URL, tlsCAFile=ca)
            db = mongo_client[database]
            coll = db[collection]
            
            # Insert records
            result = coll.insert_many(records)
            return len(result.inserted_ids)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    # File and Database configurations
    FILE_PATH = "Network_Data/dataset_full.csv"
    DATABASE = "SANJAYR"
    COLLECTION = "Network_Data"

    try:
        network_obj = NetworkDataExtract()
        
        # Extract records
        records = network_obj.csv_to_json(file_path=FILE_PATH)
        print(f"Total records to insert: {len(records)}")

        # Insert into MongoDB
        no_of_records = network_obj.insert_to_mongodb(collection=COLLECTION, database=DATABASE, records=records)
        print(f"Successfully inserted {no_of_records} records into MongoDB.")
    except Exception as e:
        print(f"Error: {str(e)}")
