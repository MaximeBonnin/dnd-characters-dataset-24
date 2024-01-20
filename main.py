
from pprint import pprint
import json
from pymongo import MongoClient, UpdateOne
from parse_character import parse_character
import asyncio
import aiohttp
from async_get import get_chars_by_id, async_get
import time

# this is terrible and I should learn how to use env vars
from my_secrets import user_name, password

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = f"mongodb+srv://{user_name}:{password}@cluster0.qdbpxyz.mongodb.net/?retryWrites=true&w=majority"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client["dnd_characters"]


def insert_character(collection_name, char_to_save:dict):
    collection_name.insert_one(char_to_save)
    print("Inserted")


def insert_multiple_characters(collection, chars_to_save:list):
    # Preparing bulk operations
    bulk_operations = []
    for data in chars_to_save:
        # Assuming each `data` item is a dictionary and has 'char_id'
        filter = {'char_id': data['char_id']}
        update = {'$set': data}
        bulk_operations.append(UpdateOne(filter, update, upsert=True))

    # Performing bulk write
    if bulk_operations:
        try:
            result = collection.bulk_write(bulk_operations)
            print(f"Inserted/Updated {result.modified_count} documents.")
        except Exception as e:
            print(f"An error occurred: {e}")
    print("Inserted")

def process_character_batch(db_collection, batch_ids:list):
    start_time = time.time()
    print(f"Staring batch...")

    # get all info
    print(f"[{round(time.time()-start_time, 2)}] Getting data...")
    reponse_list = asyncio.run(get_chars_by_id(batch_ids))

    # parse characters
    print(f"[{round(time.time()-start_time, 2)}] Parsing data...")
    list_of_parsed_characters = []
    for c in reponse_list:
        parsed_char = parse_character(reponse_tuple=c)
        list_of_parsed_characters.append(parsed_char)

    # save batch to DB
    print(f"[{round(time.time()-start_time, 2)}] Saving data...")
    insert_multiple_characters(collection=db_collection, chars_to_save=list_of_parsed_characters)

    print(f"[{round(time.time()-start_time, 2)}] Batch done")


def main():
    print("Starting...")

    # Get the database
    dbname = get_database()
    collection_name = dbname["characters"]
    # collection_name.create_index([("char_id")], unique=True)

    query = {"status_code": 200}
    count = collection_name.count_documents(query)
    print(count)
    fail_id = "25755028"
    char_id = "25755022"

    start = 0
    char_ids = ["{:08d}".format(i) for i in range(start, start+10_000)]
    #print(char_ids)
    # process_character_batch(db_collection=collection_name, batch_ids=char_ids)
    





if __name__ == "__main__":
    main()