
from pprint import pprint
import json
from pymongo import MongoClient, UpdateOne, errors
from parse_character import parse_character
import asyncio
import aiohttp
from async_get import get_chars_by_id, async_get
import time
import logging
import io
logging.basicConfig(level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    #filename='app.log',  # Log to a file named 'app.log'. Remove this to log to console.
                    filemode='a')  # 'a' for append mode, 'w' for write mode


# this is terrible and I should learn how to use env vars
from my_secrets import user_name, password

def get_database():
 
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = f"mongodb+srv://{user_name}:{password}@cluster0.qdbpxyz.mongodb.net/?retryWrites=true&w=majority"

    try:
        # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
        client = MongoClient(CONNECTION_STRING)

    except errors.ConnectionFailure as e:
        logging.error(e)

    # Create the database for our example (we will use the same database throughout the tutorial
    return client["dnd_characters"]


def insert_character(collection_name, char_to_save:dict):
    try:
        collection_name.insert_one(char_to_save)
        logging.info("Character inserted")

    except errors as e:
        logging.error(e)


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
            logging.info(f"Inserted/Updated {result.modified_count} documents.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")

    logging.info("Batch inserted.")


def process_character_batch(db_collection, batch_ids:list):
    start_time = time.time()
    logging.info(f"Staring batch...")

    try:

        # get all info
        logging.info(f"[{round(time.time()-start_time, 2)}] Getting data...")
        reponse_list = asyncio.run(get_chars_by_id(batch_ids))

        # parse characters
        logging.info(f"[{round(time.time()-start_time, 2)}] Parsing data...")
        list_of_parsed_characters = []
        for c in reponse_list:
            parsed_char = parse_character(reponse_tuple=c)
            list_of_parsed_characters.append(parsed_char)

        # save batch to DB
        logging.info(f"[{round(time.time()-start_time, 2)}] Saving data...")
        insert_multiple_characters(collection=db_collection, chars_to_save=list_of_parsed_characters)

        logging.info(f"[{round(time.time()-start_time, 2)}] Batch done")

    except Exception as e:
        logging.error(f"Error occurred: {e}")


def main():
    logging.info("Starting...")

    start = 0
    batch_size = 10_000
    number_of_batches = 100

    logging.info(f"{start=} {batch_size=} {number_of_batches=}")
    confirm = input(f"This will send {batch_size*number_of_batches} requests. Press 'Y' to confirm\n")
    if confirm == "Y":
        logging.info(f"{batch_size*number_of_batches} requests confirmed")
        for i in range(number_of_batches):
            logging.info(f"Batch {i} starting...")
            # Get the database
            dbname = get_database()
            collection_name = dbname["characters"]

            char_ids = ["{:08d}".format(i) for i in range(start, start + batch_size)]
            #print(char_ids)
            process_character_batch(db_collection=collection_name, batch_ids=char_ids)
    





if __name__ == "__main__":
    main()