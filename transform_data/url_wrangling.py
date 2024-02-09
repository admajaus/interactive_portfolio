import pandas as pd
import re
from global_structures import dtype_dct

def parse_url(loc_og_df):
    # extract all url parameters using regex
    # '[\?|&]([^=]+) where a '?' or '&' is found, extract characters until a '=' is found
    columns = loc_og_df['landingPagePlusQueryString'].str.extractall('[\?|&]([^=]+)')[0].unique()

    # initialize a list to hold values for each url parameter
    param_dfs_list = []

    # for each parameter in the url, extract the argument
    for col in columns:

        # create a regex pattern to capture all characters until a '=' is found;
        url_arg_pattern = fr'{col}=([^&]+)'

        # Extract the value from each url parameter using the defined regex pattern
        extract = loc_og_df['landingPagePlusQueryString'].str.extract(url_arg_pattern)

        # append the value extracted from the url into a list
        param_dfs_list.append(extract)

    # cat all dfs in param_dfs_list to form a single df
    url_df_parsed_loc = pd.concat(param_dfs_list, axis=1)

    # update the column names of df to match each url parameters - these are listed in an array saved as 'columns'
    url_df_parsed_loc.columns = columns

    return url_df_parsed_loc

def cat_url_df(url_df_parsed_loc, df1):
    # there are extra, unexpected parameters. In total, these params make-up less than 1% of the data
    url_df_parsed_loc.count().sort_values()

    # retain only the relevant url params from url_df_parsed in the analysis
    relevant_url_df = url_df_parsed_loc[['surface_type', 'surface_detail', 'surface_inter_position',
                    'surface_intra_position']].copy()

    # assign efficient dtypes to new df to reduce processing, memory overhead
    for col in relevant_url_df:
        relevant_url_df[col] = relevant_url_df[col].astype(dtype_dct[col])


    # concat df 'left' containing relevant url params with the original dataframe
    cated_df_loc = pd.concat(objs=(df1, relevant_url_df), axis=1)

    # Insert'landingPagePlusQueryString' next to column 'surface_type'
    index_sd = cated_df_loc.columns.get_loc('surface_type')

    shopify_url = cated_df_loc['landingPagePlusQueryString'].copy()

    index_st = cated_df_loc.columns.get_loc('surface_type')

    cated_df_loc.insert(loc=index_st, value=shopify_url, column='LandingPagePlusQueryString')

    # Delete the now redundant landingPagePlus Query String column
    cleaned_cated_df_loc = cated_df_loc.drop(columns='landingPagePlusQueryString')

    return cleaned_cated_df_loc

def url_encoding_removal(cated_url_df_loc, parsed_url_df_loc):
    # create list of columns that are shared between url_df and df
    url_cols = parsed_url_df_loc.columns.intersection(cated_url_df_loc.columns)

    # which of the cols in df are a url parameter AND have an object dtype:
    url_object_cols = cated_url_df_loc[url_cols].dtypes[cated_url_df_loc[url_cols].dtypes != 'Int8'].index

    # regex pattern to find url encoding
    non_alphanum = r'\W\d*'

    # regex pattern to find extra spaces
    no_extra_spaces = r'^\s+|\s{2,4}|\s+$'

    # for each url parameter that has dtype object:
    for col in url_object_cols:
        # replace a url encoding with a space
        cated_url_df_loc[col] = cated_url_df_loc[col].str.replace(pat=non_alphanum, repl=' ', regex=True, flags=re.I)

        # replace all extra spaces with no space
        cated_url_df_loc[col] = cated_url_df_loc[col].str.replace(pat=no_extra_spaces, repl='', regex=True, flags=re.I)

    # assign efficient dtypes early on to reduce memory and processing overhead
    for col in cated_url_df_loc.columns:
        # for each col in df1, assign the dtype using the dtype_dct
        cated_url_df_loc[col] =cated_url_df_loc[col].astype(dtype_dct[col])

    return cated_url_df_loc