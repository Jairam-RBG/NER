import os

import pandas as pd

os.chdir('C:/Users/Shyam R/NER/final_csv_1')

# loading dataframes
df1 = pd.read_csv('final_sample.csv')
df2 = pd.read_csv('final_csv_1/final_df.csv')

# deleting unwanted columns
df1.drop(["Unnamed: 0", "tags", "counts"], axis=1, inplace=True)
df2.drop("Unnamed: 0", axis=1, inplace=True)

print(df2)
# data processing for mapping
df2['resource_id'] = df2['resource_id'].str.replace(r'<http://', '', regex=True)
df2['resource_id'] = df2['resource_id'].str.replace(r'.dbpedia.org/resource/', '<>', regex=True)
df2["resource"] = df2["resource"].str.strip("[''.]")
df2.to_csv('short_abstract.csv')
df1['re_id'] = df1['re_id'].str.replace(r"[\"\'\\\],]", '')

