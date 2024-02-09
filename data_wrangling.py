import pandas as pd
pd.set_option('display.max_columns', None)
import pyarrow.parquet as pq

from gather_data.api_call import call_api
from transform_data.df_creation import create_df
from transform_data.url_wrangling import parse_url, cat_url_df, url_encoding_removal
from transform_data.correct_categorization_errors import add_new_channel_group, fix_surface_type_dupe, channel_group_assign_unassigned
from transform_data.general_cleaning import misc_cleaning

def get_transform_data():

    api_re = call_api()

    og_df = create_df(api_re)

    parsed_url_df = parse_url(og_df)

    cated_url_df = cat_url_df(parsed_url_df, og_df)

    removed_url_encoding = url_encoding_removal(cated_url_df, parsed_url_df)

    new_category = add_new_channel_group(removed_url_encoding)

    fixed_dupe = fix_surface_type_dupe(new_category)

    assigned_channel_group = channel_group_assign_unassigned(fixed_dupe)

    final_df = misc_cleaning(assigned_channel_group)

    return locals()

gtd_dict = get_transform_data()

# delete redundant api_re; the api response is saved as a dataframe in og_df
del gtd_dict['api_re']

# serialize each dataframe into a apache parquet file 
# Keys: DataFrame name, Values: DataFrame
for keys, values in gtd_dict.items():
     values.to_parquet(path = rf'parquet_objects\{keys}.parquet')

#print(gtd_dict['removed_url_encoding'].columns)
# print(gtd_dict['final_df']['channel_group'].value_counts())
#print(gtd_dict['cated_url_df']['surface_type'].value_counts()),
# print(gtd_dict['final_df']['surface_detail'].value_counts())

# #Measuring execution time
# import timeit
# execution_time = timeit.timeit('get_transform_data()', globals=globals(), number=1)
# print(f"Execution time: {execution_time} seconds")
