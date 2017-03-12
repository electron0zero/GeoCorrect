import pandas as pd
import sqlite3

print("please remove any existing db.sqlite file before running this script, this script will create a new file with data from csv files")

print("opening database connection")

db = sqlite3.connect('db.sqlite')

print("writing checkins to db")
checkins_df = pd.read_csv('clean_checkins.csv')
checkins_df.to_sql('checkins', db)

print("writing venues to db")
loc_df = pd.read_csv('de_duplicated_location.csv')
loc_df.to_sql('venues', db)
