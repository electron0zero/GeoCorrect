import pandas as pd

file1 = "../dataset/dataset_TSMC2014_NYC.txt"
file2 = "../dataset/dataset_TSMC2014_TKY.txt"

# it will a list of lists of checkins
newLines = []
# checkin list, reset after appending in newLines
checkin = []

print("Reading file: {}".format(file1))

with open(file1) as input_file1:
    for line in input_file1:
        newLine = [x.strip() for x in line.split('\t')]
        # build a checkin list
        checkin.append(newLine[1])
        checkin.append(newLine[4])
        checkin.append(newLine[5])
        # add that list to newLines list makeing it list of checkin lists
        newLines.append(checkin)
        # reset checkin list for next checkin
        checkin = []

print("Reading file : {}".format(file2))
with open(file2) as input_file2:
    for line in input_file2:
        newLine = [x.strip() for x in line.split('\t')]
        # build a checkin list
        checkin.append(newLine[1])
        checkin.append(newLine[4])
        checkin.append(newLine[5])
        # add that list to newLines list makeing it list of checkin lists
        newLines.append(checkin)
        # reset checkin list for next checkin
        checkin = []

# put the data in a dataframe and then in a csv file
# NOTE: don't forget to add header in finished CSV FILE
print("Found {} Checkin Entries in file".format(len(newLines)))
print("building CSV file")
my_df = pd.DataFrame(newLines)
# print(my_df)
my_df.to_csv('checkins.csv', index=False, header=False)

print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("NOTE: don't forget to add header in finished CSV file")
print("see readme file for instructions")
print("+++++++++++++++++++++++++++++++++++++++++++++++++++++")
