import pandas as pd
import sqlite3

print("opening database connection")

db = sqlite3.connect('db.sqlite')

print("writing results to db")
results_df = pd.read_csv('results.csv')
results_df.to_sql('results', db)
