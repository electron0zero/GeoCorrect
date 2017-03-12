import pandas as pd

my_df = pd.read_csv('de_duplicated_location.csv')

df1 = my_df[['venue_id']]
print(len(df1))
df1.to_csv('venue_id_from_location.csv', index=False, header=True)
