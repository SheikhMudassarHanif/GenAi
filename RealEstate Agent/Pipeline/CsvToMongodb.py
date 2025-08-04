import pandas as pd
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# Load environment variables

def InsertData(city:str, page:int):
    load_dotenv()

    MONGO_URI = os.getenv('MONGO_URI')
    DB_NAME = os.getenv('DB_NAME')
    COLLECTION_NAME = os.getenv('COLLECTION_NAME')

    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    collection = db[COLLECTION_NAME]
    print(city)
    # Read CSV
    df = pd.read_csv(f'data/Cleaned_{city}_PropertyDataComplete{page}.csv')

    # charlotte
    # NC_PropertyDataComplete2.csv
    # Convert DataFrame to dictionary records
    data = df.to_dict(orient='records')

    # Insert into MongoDB
    collection.insert_many(data)

    print(f"✅ Inserted {len(data)} records into {DB_NAME}.{COLLECTION_NAME}")
