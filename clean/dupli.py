import pandas as pd
loc_df = pd.read_csv('merged_location.csv')
clean_df = loc_df.drop_duplicates(subset=['venue_id'])
clean_df.to_csv("de_duplicated_location.csv", index=False, header=True)
