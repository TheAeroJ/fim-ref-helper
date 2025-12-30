import dataset
from dotenv import load_dotenv
import argparse
import os

# Get environment variables; important for defining location of database
load_dotenv()

dbpath = os.getenv("dbpath")

db = dataset.connect(dbpath)

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

events = db.create_table('events', primary_id='id', primary_type='Integer')
events.create_column('city', type=db.types.string, nullable=False)
events.create_column('country', type=db.types.string, nullable=False)
events.create_column('district', type=db.types.string, nullable=True)
events.create_column('end_date', type=db.types.date, nullable=False)
events.create_column('event_code', type=db.types.string, nullable=False)
events.create_column('event_type', type=db.types.integer, nullable=False)
events.create_column('key', type=db.types.string, nullable=False, unique=True)
events.create_column('name', type=db.types.string, nullable=False)
events.create_column('start_date', type=db.types.date, nullable=False)
events.create_column('state_prov', type=db.types.string, nullable=True)
events.create_column('year', type=db.types.integer, nullable=False)
events.create_column('end_DoW', type=db.types.string, nullable=False)

print("Tables in the database: " + str(db.tables))
print("Columns in events table: " + str(events.columns))

# Table people {
#   id int [primary key, unique]
#   first_name text [not null]
#   last_name text [not null]
#   phone numeric
#   rookie_season int [default: null]
#   ref_role enum
# }



# Table users {
#   id int [primary key, unique]
#   person_id int [unique]
#   site_role enum
# }