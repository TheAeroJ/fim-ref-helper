
from dotenv import load_dotenv
import argparse
import os
import sqlalchemy

# Get environment variables; important for defining location of database
# TODO: Figure out whether these things should be passed as arguments instead?
load_dotenv()
dbpath = os.getenv("dbpath")

def db_create():
    # Use DDL (Data Definition Language) Statements to create the database schema
    # Set up initial return dictionary
    results_dict = {
        "status" : 1,
        "message" : "Database creation failed."
        }

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
        events_table = sqlalchemy.Table(
            'events',
            db_metadata_obj,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, nullable=False, unique=True),
            sqlalchemy.Column('city', sqlalchemy.Text),
            sqlalchemy.Column('country', sqlalchemy.Text),
            sqlalchemy.Column('district', sqlalchemy.Text),
            sqlalchemy.Column('end_date', sqlalchemy.Numeric),
            sqlalchemy.Column('event_code', sqlalchemy.Text),
            sqlalchemy.Column('event_type', sqlalchemy.Integer),
            sqlalchemy.Column('key', sqlalchemy.Text, nullable=False, unique=True),
            sqlalchemy.Column('name', sqlalchemy.Text),
            sqlalchemy.Column('start_date', sqlalchemy.Numeric),
            sqlalchemy.Column('state_prov', sqlalchemy.Text),
            sqlalchemy.Column('year', sqlalchemy.Integer, nullable=False),
            sqlalchemy.Column('end_DoW', sqlalchemy.Text, nullable=False)
        )

        # Create the People table

        # Table people {
        #   id int [primary key, unique]
        #   first_name text [not null]
        #   last_name text [not null]
        #   phone numeric
        #   rookie_season int [default: null]
        #   ref_role enum
        # }
        people_table = sqlalchemy.Table(
            'people',
            db_metadata_obj,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, nullable=False, unique=True),
            sqlalchemy.Column('first_name', sqlalchemy.Text, nullable=False),
            sqlalchemy.Column('last_name', sqlalchemy.Text, nullable=False),
            sqlalchemy.Column('phone', sqlalchemy.Numeric),
            sqlalchemy.Column('rookie_season', sqlalchemy.Integer, default=None),
            sqlalchemy.Column('ref_role', sqlalchemy.Text)
        )

        # NOTE: need to ensure we validate that the 'ref_role' values are defined properly

        # Table users {
        #   id int [primary key, unique]
        #   person_id int [unique]
        #   site_role enum
        # }
        users_table = sqlalchemy.Table(
            'users',
            db_metadata_obj,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, nullable=False, unique=True),
            sqlalchemy.Column('person_id', sqlalchemy.ForeignKey('people.id'), unique=True),
            sqlalchemy.Column('site_role', sqlalchemy.Text)
        )
        # NOTE: need to ensure we validate that the 'site_role' values are defined properly

        crew_table = sqlalchemy.Table(
            'crew',
            db_metadata_obj,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, nullable=False, unique=True),
            sqlalchemy.Column('event_id', sqlalchemy.ForeignKey('events.id')),
            sqlalchemy.Column('person_id', sqlalchemy.ForeignKey('people.id')),
            sqlalchemy.Column('role', sqlalchemy.Text)
        )

        # Create all tables in the database?
        try:
            db_metadata_obj.create_all(engine)
        except Exception as e:
            results_dict["message"] = f"Database creation failed: {e}"
        else:
            results_dict["status"] = 0
            results_dict["message"] = "Database created successfully."

    return results_dict

def db_modify(args_dict):
    # Need to think about what arguments I need in my modify function
    # DML (Data Manipulation Language) Statements to modify the database schema or data
    # Set up default as failure case
    results_dict = {
        "status" : 1,
        "message" : "Database modification failed."
        }

    # What are we returning? Status code? Other data?
    
    return results_dict

def db_query(args_dict):
    # DQL (Data Query Language) Statements to query the database schema or data
    results_dict = {
        "status" : 1,
        "message" : "Database query failed."
        }

    # We should be returning a status code and the queried data
    return results_dict

def db_interact(mode, args):
    # Logic to figure out whether we are setting up our db for the first time or whether we are working with the existing db
    if mode == "create":
        db_create()
    elif mode == "modify":
        # Do stuff
        db_modify(args)
        return
    elif mode == "query":
        # Do stuff
        db_query(args)
        return
    else:
        # Do stuff
        return
    
if __name__ == "__db_interact__":
    parser = argparse.ArgumentParser(description="Database Setup Script")
    parser.add_argument('--mode', type=str, help='Mode to run the script in: create, modify, query', required=True)
    parser.add_argument('--args', type=dict, help='Arguments for modify or query modes', required=False, default={})
    # TODO: Consider adding an additional argument for environment variables such as the database path?
    args = parser.parse_args()
    db_interact(args.mode , args.args)