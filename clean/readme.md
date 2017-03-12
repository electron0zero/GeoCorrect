This folder contains scripts for
- cleaning and per-processing of dataset
- create SQLite Database file with dataset

--------
run `clean.py` it will produce a `checkin.csv` file

number of entries should be equal to (227428 + 573703 = 801131) from both files

then open csv file and header on it
(you can add this below line as it is)
venue_id,lat,lng

-------
then run `build_SQL_DB.py`

-------
get_venue_id.py is for extracting unique venue_id from db.

we should get 100191 unique venues from 801131 check-ins
