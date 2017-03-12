# get location of a place provided it's foursquare id
# it is used to get groundtruth value of location
import requests
import json
import datetime
import time
import pandas as pd
from twilio.rest import TwilioRestClient


now = datetime.datetime.now()
print("Started On")
print(str(now))

# venue_id = "51140198e4b0874a568cde81"
# we are making useless requests to foursquare API
c_id = "<client_id>"
c_sec = "<client_secret>"
v = "20170101"
payload = {'client_id': c_id, 'client_secret': c_sec, 'v': v}
base_url = "https://api.foursquare.com/v2/venues/"

limit_rem = 10
final_data = []
outfilename = "outdata_"
# open venue_id file
urls_file = open('venue_id.txt')
# print(urls_file)
try:
    for item in urls_file:
        venue_id = item.strip()
        print(venue_id, end="\t")
        # time.sleep(0.5)
        r = requests.get(base_url + venue_id, params=payload)
        # print(r.status_code)
        # print(r.headers['content-type'])
        # print(r.headers['X-RateLimit-Remaining'])
        limit_rem = int(r.headers['X-RateLimit-Remaining'])
        print(limit_rem, end="\t")
        print(r.status_code)
        if (r.status_code == 200) and limit_rem > 1:
            resp = r.json()
            # print(venue_id)
            real_loc = []
            real_loc.append(resp['response']['venue']['id'])
            real_loc.append(resp['response']['venue']['location']['lat'])
            real_loc.append(resp['response']['venue']['location']['lng'])
            final_data.append(real_loc)
            # print(real_loc)
        else:
            # wait till rate limit is expired it is 5000 request per hour
            print("Sleeping for an hour")
            print("building CSV file of data till now")
            my_df = pd.DataFrame(final_data)
            timeNow = str(int(time.time()))
            my_df.to_csv(outfilename + timeNow, index=False, header=True)
            # time.sleep(1800)
            print("Resuming Operation back at")
            timeNow = str(int(time.time()))
            print(timeNow)
    print("Done - building CSV file")
    my_df = pd.DataFrame(final_data)
    timeNow = str(int(time.time()))
    my_df.to_csv(outfilename + timeNow, index=False, header=True)
except:
    print("Got an Exception Saving data till Now")
    print("building CSV file of data till now")
    my_df = pd.DataFrame(final_data)
    timeNow = str(int(time.time()))
    print(timeNow)
    my_df.to_csv(outfilename + timeNow, index=False, header=True)
    # put your own Twilio credentials here
    ACCOUNT_SID = '<ACCOUNT_SID>'
    AUTH_TOKEN = '<AUTH_TOKEN>'
    client = TwilioRestClient(ACCOUNT_SID, AUTH_TOKEN)
    client.messages.create(
        to='<TO_PHONE_NO>',
        from_='<Twilio_PHONE_NO>',
        body='<MESSAGE_BODY>',
    )
    raise
