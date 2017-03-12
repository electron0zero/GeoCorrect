import pandas as pd

venue_id_loc_file = 'venue_id_from_location.csv'
checkins_file = 'checkins.csv'

# get all the venue_id from loc file into a list
venue_id = []
with open(venue_id_loc_file) as loc_file:
    for line in loc_file:
        venue_id.append(line.strip())

# get all checkins in list if that venue id is in venue_id list
clean_checkins = []
with open(checkins_file) as file2:
    for checkin in file2:
        checkin = [x.strip() for x in checkin.split(',')]
        v_id = checkin[0]
        if v_id in venue_id:
            clean_checkins.append(checkin)

# check lengths
print("venue_id length")
print(len(venue_id))
print("clean_checkins length")
print(len(clean_checkins))
print("building CSV file")
my_df = pd.DataFrame(clean_checkins)
# print(my_df)
my_df.to_csv('clean_checkins.csv', index=False, header=False)

print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("NOTE: don't forget to add header in finished CSV file")
print("see readme file for instructions")
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
