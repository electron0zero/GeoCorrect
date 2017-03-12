import pandas as pd
import glob
import time
import sys

# print(sys.argv[1:])

# put file in order you want them to be merged
# un comment below 'files = sys.argv' line and comment `files = []` list
# if you want to pass file names by command line arguments
# files = sys.argv[1:]
# files = []
# crawl all the files with outdata in file name
files = [file for file in glob.glob("outdata*")]
print(files)
print(len(files))
if len(files):
    # it will a list of lists of checkins
    newLines = []
    newLine = []
    # checkin list, reset after appending in newLines
    # checkin = []
    for file in files:
        print("Reading file: {}".format(file))
        with open(file) as input_file:
            for line in input_file:
                newLine = [x.strip() for x in line.split(',')]
                # build a checkin list
                # checkin.append(newLine[1])
                # checkin.append(newLine[4])
                # checkin.append(newLine[5])
                # add that list to newLines list makeing it list of checkin lists
                newLines.append(newLine)
                # reset checkin list for next checkin
                newLine = []

    # put the data in a dataframe and then in a csv file
    # NOTE: don't forget to add header in finished CSV FILE
    print("Found {} Entries in files".format(len(newLines)))
    print("building CSV file")
    my_df = pd.DataFrame(newLines)
    # print(my_df)
    timeNow = str(int(time.time()))
    outfilename = "merged_location.csv"
    my_df.to_csv(outfilename, index=False, header=False)
else:
    print("provide file names as argument")
