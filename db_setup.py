
from dotenv import load_dotenv
import argparse
import os
import sqlalchemy

# Get environment variables; important for defining location of database
load_dotenv()

dbpath = os.getenv("dbpath")

def generateSqlCommand(stringList):
    return "".join(stringList)

def main():

    # Create the metadata object to use for our database
    db_metadata_obj = sqlalchemy.MetaData()
    # Create the database engine
    engine = sqlalchemy.create_engine("sqlite+pysqlite:///" + dbpath, echo=True)

    with engine.begin() as connection:
        # Everything needs to be done inside this block for initial database setup

        # Define the database schema
        # Table events {
        #   id int [primary key, not null, unique]
        #   city text
        #   country text
        #   district dictrict_object
        #   end_date numeric
        #   event_code text
        #   event_type int
        #   key text [not null, unique]
        #   name text
        #   start_date numeric
        #   state_prov text
        #   year int [not null]
        #   end_DoW text [not null]
        # }
        # Construct the giga string for creating the events table in a manner which is readable
        eventsCreationStrings = [
            "CREATE TABLE events (",
            "id INTEGER PRIMARY KEY NOT NULL UNIQUE, ",
            "city TEXT, ",
            "country TEXT, ",
            "district TEXT, ",
            "end_date NUMERIC, ",
            "event_code TEXT, ",
            "event_type INTEGER, ",
            "key TEXT NOT NULL UNIQUE, ",
            "name TEXT, ",
            "start_date NUMERIC, ",
            "state_prov TEXT, ",
            "year INTEGER NOT NULL, ",
            "end_DoW TEXT NOT NULL)"
        ]
        eventGigaString = generateSqlCommand(eventsCreationStrings)
        connection.execute(sqlalchemy.text(eventGigaString))

        # Create the People table

        # Table people {
        #   id int [primary key, unique]
        #   first_name text [not null]
        #   last_name text [not null]
        #   phone numeric
        #   rookie_season int [default: null]
        #   ref_role enum
        # }

        peopleCreationStrings = [
            "CREATE TABLE people (",
            "id INTEGER PRIMARY KEY NOT NULL UNIQUE, ",
            "first_name TEXT NOT NULL, ",
            "last_name TEXT NOT NULL, ",
            "phone NUMERIC, ",
            "rookie_season INTEGER DEFAULT NULL, ",
            "ref_role TEXT)"
        ]

        peopleGigaString = generateSqlCommand(peopleCreationStrings)
        connection.execute(text(peopleGigaString))

        # NOTE: need to ensure we validate that the 'ref_role' values are defined properly

        # Table users {
        #   id int [primary key, unique]
        #   person_id int [unique]
        #   site_role enum
        # }

        usersCreationStrings = [
            "CREATE TABLE users (",
            "id INTEGER PRIMARY KEY NOT NULL UNIQUE, ",
            "person_id INTEGER UNIQUE, ",
            "site_role TEXT)"
        ]

        usersGigaString = generateSqlCommand(usersCreationStrings)
        connection.execute(text(usersGigaString))

        # NOTE: need to ensure we validate that the 'site_role' values are defined properly

        connection.commit()

    

        # Table users {
        #   id int [primary key, unique]
        #   person_id int [unique]
        #   site_role enum
        # }

    return
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Database Setup Script")
    args = parser.parse_args()
    main()