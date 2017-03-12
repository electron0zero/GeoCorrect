import sqlite3
from more_itertools import unique_everseen
import pandas as pd

connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()
cursor.execute("SELECT * FROM checkins")
rows = cursor.fetchall()
venue_id = []
for row in rows:
    # print(row[1])
    venue_id.append(row[1])

print("total venue_id in checkins : {}".format(len(venue_id)))
venue_id = unique_everseen(venue_id)
print("building CSV file")
my_df = pd.DataFrame(venue_id)
print("found unique venue_id : {}".format(len(my_df)))
my_df.to_csv('venue_id.csv', index=False, header=True)
