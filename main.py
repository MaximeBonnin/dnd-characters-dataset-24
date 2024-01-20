
from pprint import pprint
import json
from pymongo import MongoClient
from parse_character import parse_character

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


def main():
    print("Starting...")

    # Get the database
    dbname = get_database()
    collection_name = dbname["characters"]

    fail_id = "25755028"
    char_id = "25755022"

    parsed_char = parse_character(char_id)

    print(parsed_char)

    #insert_character(collection_name=collection_name, char_to_save=parsed_char)

    #with open("target.json", "w") as f:
    #    f.write(json.dumps(parsed_char, indent=2))






if __name__ == "__main__":
    main()