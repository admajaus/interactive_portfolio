''' deserialize parquet objects and convert into dataframes
Conduct small data manipulations readying the data for use in dashboard visualizations'''

import pandas as pd

# deserialize parquet file; convert to pandas dataframe
df_final = pd.read_parquet(path =r'parquet_objects/final_df.parquet')

# CHANNEL GROUP graph pre-processing-----------------------------------------------------------

channel_group_subset = df_final[['channel_group', 'totalUsers', 'conversions']].copy()

# Sum totalUsers, conversions by Channel Group; reset the index to move the channel group out of the index and into it's own column
channel_group_subset = channel_group_subset.groupby('channel_group', observed = False).sum().reset_index()

# create new field 'conversion rate'
channel_group_subset['conversion_rate'] = round(channel_group_subset['conversions'] / channel_group_subset['totalUsers'], 2)

# sort values by descending for aestheic/flow of visuals in bar chart
channel_group_subset.sort_values('totalUsers', ascending = False, inplace = True)

# SURFACE_TYPE graph pre-processing-----------------------------------------------------------
surface_type_subset = df_final[['surface_type', 'totalUsers', 'conversions']].copy()

# Sum totalUsers, conversions by surface_type(app section)
# reset the index so that surface_type is a feature vs. multi-index
surface_type_subset = surface_type_subset.groupby('surface_type', observed = False).sum().reset_index()

# add conversion rate as a new field to the df
surface_type_subset['conversion_rate'] = round(surface_type_subset['conversions']/ surface_type_subset['totalUsers'],2)

# sort the df by totalUsers descending
surface_type_subset.sort_values('totalUsers', ascending = False, inplace = True)


#### SURFACE_TYPE == SEARCH: Word Cloud - pre-processing----------------------------------------------

# Sum conversions by keyword; keywords found in surface_detail where surface_type == search
keyword_conversions = df_final.query('surface_type =="search"').groupby('surface_detail')['conversions'].sum()

# convert the keywords to a dictionary for use in a word cloud
keyword_wordcloud_dict = keyword_conversions.to_dict()

#### SURFACE_TYPE == SEARCH: Keyword Table - pre-processing----------------------------------------------

# query the dataframe to return records with search terms
# sum conversions and totalUsers per keyword
# reset index to remove keywords as index and set as column
keyword_df = df_final.query('surface_type =="search"').groupby('surface_detail')[['totalUsers','conversions']].sum().reset_index()

# add conversion_rate to keywords_df
keyword_df['conversion_rate'] = round(keyword_df['conversions'] / keyword_df['totalUsers'],2)

# focus on non-negligible totalUsers
keyword_df = keyword_df.query('totalUsers > 9')

# Identify outlier conversion rates and their index in the df
to_drop = keyword_df.query('conversion_rate > 2').index

# drop the outlier conversion rates based on their index
keyword_df = keyword_df.drop(index=to_drop)


#SURFACE TYPE TIME SERIES pre-processing_____________________________________________________
# Set date column to date-time data type
df_final['date'] = pd.to_datetime(df_final['date'])

# Set the data as the index
df_final.set_index('date', inplace=True)

resampled_dfs = {
    # Create a time series for each surface_type
    # Up-sample the dataframe by 2 weeks and sum by totalUsers and Conversions
    # Add conversion_rate as a column in the dataframe
    # Convert the dtype of conversion rate to a float; when deserializing the dataframe into a df, null values in columns with categorical dtypes won't be recognized as null
    # fill the nulls with 0
    surface_type: df_final.query(f'surface_type == "{surface_type}"')
    .resample('2W')
    .agg({'totalUsers': 'sum', 'conversions': 'sum'})
    .assign(conversion_rate=lambda x: x['conversions'] / x['totalUsers'])
    .astype({'conversion_rate': 'float'})
    .fillna(0)
    for surface_type in df_final['surface_type'].unique()
}

### SURFACE DETAIL PER SURFACE TYPE(NON SEARCH) pre-processing-------------------

# Create a data_table for each surface_type(non-search)
# For each surface_type, group by surface_detail and sum totalUsers and conversion
# add conversion rate as a column in the dataframe
# reset the index to move the surface_detail out of the index and into it's own column
# Convert the dtype of conversion rate to a float; when deserializing the dataframe into a df, null values in columns with categorical dtypes won't be recognized as null
# fill the nulls with 0
app_section_detail = {
    type:
    df_final.query(f'surface_type == "{type}"')
    .groupby('surface_detail')[['totalUsers', 'conversions']].sum()
    .reset_index()
    .assign(conversion_rate = lambda x: round(x['conversions'] / x['totalUsers'],4))
    .astype({'conversion_rate':'float'})
    .assign(conversion_rate=lambda x: x['conversion_rate']
    .fillna(0))

for type in df_final['surface_type'].unique()
}

#INT*ER-POSITION PER APP SECTION(surface_type)-------------------------
# Create a data_table for each surface_type(non-search), grouped by inter-position, sum totalUsers and conversions
# reset the index to move inter_position into its own column so it shows in the dash_table
# add a conversion rate column to the dataframe
# Convert the dtype of conversion rate to a float; when deserializing the dataframe into a df, null values in columns with categorical dtypes won't be recognized as null
# fill the nulls with 0
inter_position = {
    type:
    df_final.query(f'surface_type == "{type}"')
    .groupby('surface_inter_position')[['totalUsers', 'conversions']].sum()
    .reset_index()
    .assign(conversion_rate = lambda x: round(x['conversions'] / x['totalUsers'],4))
    .astype({'conversion_rate':'float'})
    .assign(conversion_rate=lambda x: x['conversion_rate']
    .fillna(0))

for type in df_final.surface_type.unique()

}

# INT*RA*-POSITION PER APP SECTION(surface_type)-------------------------
# Create a data_table for each surface_type(non-search), grouped by intra-position, sum totalUsers and conversions
# reset the index to move inter_position into its own column so it shows in the dash_table
# add a conversion rate column to the dataframe
# Convert the dtype of conversion rate to a float; when deserializing the dataframe into a df, null values in columns with categorical dtypes won't be recognized as null
# fill the nulls with 0
intra_position = {
    type:
        df_final.query(f'surface_type == "{type}"')
        .groupby('surface_intra_position')[['totalUsers', 'conversions']].sum()
        .reset_index()
        .assign(conversion_rate=lambda x: round(x['conversions'] / x['totalUsers'], 2))
        .fillna(0)
        .astype({'conversion_rate': 'float'})
        .assign(conversion_rate=lambda x: x['conversion_rate'].fillna(0))

    for type in df_final.surface_type.unique()

}