"""
A script and module to handle database operations for the FIM Referee Helper application.
"""
from dotenv import load_dotenv
import argparse
import os
import sqlalchemy

# Other TODOs:
# - Add logging instead of print statements
# - Add error handling for database operations
# - Look into Alembic for database migrations and updates...maybe overkill for now?

# Get environment variables; important for defining location of database
# TODO: Figure out whether these things should be passed as arguments instead?
load_dotenv()
dbpath = os.getenv("dbpath")
print("Database path from .env file: ", dbpath)

def args_validate(args_dict):
    # Validate the arguments passed in the args_dict
    # Ensure required arguments are present and valid
    pass

def db_create(args_dict):
    # Use DDL (Data Definition Language) Statements to create the database schema
    # Set up initial return dictionary
    results_dict = {
        "status" : 1,
        "message" : "Database creation failed."
        }
    
    db_metadata_obj = args_dict["db_metadata_obj"]
    engine = args_dict["engine"]

    with engine.begin() as connection:
        # Everything needs to be done inside this block for initial database setup

        # Define the database schema
        # Events table
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

        # Create the Users table
        users_table = sqlalchemy.Table(
            'users',
            db_metadata_obj,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, nullable=False, unique=True),
            sqlalchemy.Column('person_id', sqlalchemy.ForeignKey('people.id'), unique=True),
            sqlalchemy.Column('site_role', sqlalchemy.Text)
        )
        # NOTE: need to ensure we validate that the 'site_role' values are defined properly

        # Create the Volunteer Assignments table
        volunteer_assignments = sqlalchemy.Table(
            'volunteer_assignments',
            db_metadata_obj,
            sqlalchemy.Column('id', sqlalchemy.Integer, primary_key=True, nullable=False, unique=True),
            sqlalchemy.Column('event_id', sqlalchemy.ForeignKey('events.id')),
            sqlalchemy.Column('person_id', sqlalchemy.ForeignKey('people.id')),
            sqlalchemy.Column('role', sqlalchemy.Text)
        )

        # Create all tables in the database
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
    
    db_metadata_obj = args_dict["db_metadata_obj"]
    engine = args_dict["engine"]
    args = args_dict
    
    # What kind of modifications are we making?
    # Type Insertions? Updates? Deletions?
    if args.operation == "insert":
        # Handle Insertions
        # Validate input args
        # Expected args: table_name (str), values (dict)
        table_name = args.table_name
        # Expected to be a dictionary of column names and their corresponding values, or a list of such dictionaries for multiple insertions
        # NOTE: If a list of dictionaries is provided, the first dictionary will be used to validate the column names and, as such, must include ALL columns
        # TODO: Figure out whether we should do some sanitization/validation of the input intelligently
        # we want to make sure we don't have any errors with improper column names
        values = args.values

        # Confirm table exists
        if table_name not in db_metadata_obj.tables:
            results_dict["message"] = f"Table {table_name} does not exist in the database."
            return results_dict
        else:
            try:
                table = db_metadata_obj.tables[table_name]
                # NOTE: Need to validate that the keys in 'values' match the columns in the table
                with engine.begin() as connection:
                    result = connection.execute(
                        sqlalchemy.insert(table),
                        values
                    )
                    results_dict["result"] = result
            except Exception as e:
                results_dict["message"] = f"Insertion failed: {e}"
    elif args.operation == "update":
        # Handle Updates
        pass
    elif args.operation == "delete":
        # Handle Deletions
        pass
    else:
        results_dict["message"] = "Invalid operation specified."
        return results_dict


    # What are we returning? Status code? Other data?
    
    return results_dict

def db_query(args_dict):
    # DQL (Data Query Language) Statements to query the database schema or data
    results_dict = {
        "status" : 1,
        "message" : "Database query failed."
        }
    db_metadata_obj = args_dict["db_metadata_obj"]
    engine = args_dict["engine"]
    args = args_dict

    # Query the database based on the arguments provided


    # We should be returning a status code and the queried data
    return results_dict

def db_operate(mode, args):
    # Logic to figure out whether we are setting up our db for the first time or whether we are working with the existing db
    print("Operating in mode:", mode)

    # Create the metadata object to use for our database
    db_metadata_obj = sqlalchemy.MetaData()
    # Create the database engine
    engine = sqlalchemy.create_engine("sqlite+pysqlite:///" + dbpath, echo=True)

    # Append the db metadata object and engine to the args dictionary
    args.update({"db_metadata_obj": db_metadata_obj, "engine": engine})

    if mode == "create":
        db_create(args)
    elif mode == "modify":
        # Do stuff
        db_modify(args)
        return
    elif mode == "query":
        # Do stuff
        query_result = db_query(args)
        return query_result
    else:
        # Do stuff
        return
    
if __name__ == "__main__":
    print("Running db_operate.py directly from command line")
    parser = argparse.ArgumentParser(description="Database Setup Script")
    parser.add_argument('--mode', type=str, help='Mode to run the script in: create, modify, query', required=True)
    parser.add_argument('--args', type=dict, help='Arguments for modify or query modes', required=False, default={})
    # TODO: Consider adding an additional argument for environment variables such as the database path?
    args = parser.parse_args()
    print("Arguments parsed:", args)
    db_operate(args.mode , args.args)