import pandas as pd

# TABULAR: CREATE DATAFRAME TAB - data_table input--------------------------------------------
# de-serialize the dataframe
original_df = pd.read_parquet(path=r'parquet_objects/og_df.parquet')

# create a sample of the dataframe
original_df_sample = original_df.query('landingPagePlusQueryString != "(not_set)"').sample(15)

# TABULAR: URL WRANGLING TAB - data_table input--------------------------------------------
url_df = pd.read_parquet(path=r'parquet_objects/removed_url_encoding.parquet')
url_df = url_df.query('LandingPagePlusQueryString != "(not_set)"')
url_df = url_df.query('surface_detail != "nan"')

url_df_sample = url_df.sample(15)

parsed_url_sample = url_df_sample[['LandingPagePlusQueryString','surface_type','surface_detail', 'surface_inter_position', 'surface_intra_position']]


# TABULAR: RECATEGORIZE DATA TAB - data_table input--------------------------------------------
b4_recategorize = pd.read_parquet(path=r'parquet_objects/removed_url_encoding.parquet')['sessionDefaultChannelGroup'].value_counts().reset_index()

# add a grayed-out row for ease in comparing b4 and after re-categorization tables
blank_row_b4 = pd.DataFrame(data = {'sessionDefaultChannelGroup': 'App Store', 'count': '0'}, index = [0] )

# Concatenate the blank row with the b4_re-categrorize DataFrame
b4_recategorize = pd.concat([blank_row_b4, b4_recategorize], ignore_index=True)

# Create a table summarizing the counts per channel group
after_recategorize = pd.read_parquet(path =r'parquet_objects/final_df.parquet')['channel_group'].value_counts().reset_index()

index_position = b4_recategorize.query('sessionDefaultChannelGroup == "Unassigned"').index[0]

# add a grayed-out row for ease in comparing b4 and after re-categorization tables
blank_row_after = pd.DataFrame(data = {'channel_group': 'Unassigned', 'count': '0'}, index=[index_position])

# Split the DataFrame before and after index_position/ the insertion point
after1 = after_recategorize.iloc[:index_position]
after2 = after_recategorize.iloc[index_position:]

# Adjust the index of the second part of the DataFrame to accommodate the new row
after2.index = range(index_position +1, len(after_recategorize) + 1)

# Concatenate the DataFrames
after_recategorize = pd.concat([after1, blank_row_after, after2])


# TABULAR: VISUALIZATION TAB - GRAPH AND DROPDOWN input--------------------------------------------
viz_df = pd.read_parquet(path=r'parquet_objects/final_df.parquet')
viz_channel_group = viz_df['channel_group'].value_counts().reset_index()

