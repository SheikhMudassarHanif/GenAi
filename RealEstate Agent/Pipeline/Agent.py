import os
import dotenv
from langchain_groq import ChatGroq

dotenv.load_dotenv()
groq_api_key=os.getenv('GROQ_API_KEY')
langsmith_api_key=os.getenv('LANGSMITH_API_KEY')
# print(groq_api_key)

LANGSMITH_TRACING="true"
LANGSMITH_ENDPOINT="https://api.smith.langchain.com"
LANGSMITH_API_KEY="langsmith_api_key"
LANGSMITH_PROJECT="default"

print(groq_api_key)

import pandas as pd
import math
import json

def ReadInput(csv_path, collection):
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ Failed to read CSV: {e}")
        return

    for idx, row in df.iterrows():
        try:
            # Clean values
            city = str(row.get("city", "")).strip().lower()
            property_type = str(row.get("property_type", "")).strip().lower()
            subtype = str(row.get("subtype", "")).strip().lower()

            # Validate square footage
            square_footage = row.get("square_footage", None)
            try:
                square_footage = float(square_footage)
                is_valid_sqft = not math.isnan(square_footage)
            except:
                is_valid_sqft = False

            # Build query
            query_fields = {
                "city": city,
                "property_type": property_type,
                "subtype": subtype
            }

            query_fields = {
                k: v for k, v in query_fields.items()
                if v not in [None, "", "nan", "NaN"]
            }

            if is_valid_sqft:
                query_fields["square_footage"] = {"$gte": square_footage}

            print(f"🔍 Querying for: {query_fields}")
            results, avg_price = QueryDB(query_fields, collection)

            if results:
                print(f"✅ Found {len(results)} properties. Avg asking price: ${avg_price:,.2f}")
            else:
                print("❌ No matching results.")

        except Exception as e:
            print(f"⚠️ Error in row {idx}: {e}")
def QueryDB(query_fields, collection):
    """Query MongoDB with validated data input and return average asking_price."""
    try:
        cursor = collection.find(query_fields)
        results = list(cursor)

        if not results:
            return [], 0.0

        # Safely extract asking_price values
        asking_prices = []
        for item in results:
            price = item.get("price")
            if price is not None:
                try:
                    price_val = float(price)
                    if not math.isnan(price_val):
                        asking_prices.append(price_val)
                except:
                    continue  # Skip invalid price

        avg_price = sum(asking_prices) / len(asking_prices) if asking_prices else 0.0

        print("📄 Result:")
        print(json.dumps(results, indent=2, default=str))

        return results, avg_price

    except Exception as e:
        print(f"⚠️ Error during DB query: {e}")
        return [], 0.0

#
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
collection = db[COLLECTION_NAME]

ReadInput("data/input_property.csv", collection)
