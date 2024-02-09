import pandas as pd
import numpy as np
import re
from global_structures import dtype_dct

''' Traffic that is defined as a 'Direct' channel group and not null or blank in
'surface_type' should be categorized as the channel group 'App Store', NOT 'Direct'
Create a new df col 'channel_group' to incl new category 'App Store' '''

def add_new_channel_group(removed_url_encoding_loc):
    # create boolean expression: if sDCG is 'Direct' and surface_type is 'nan'
    sDCG_is_appstore = (removed_url_encoding_loc.sessionDefaultChannelGroup == 'Direct') & (removed_url_encoding_loc['surface_type'].notnull())

    # Assign 'App Store' when sDCG is Direct and surf_type is 'nan', keep original sDCG where expression is false
    channel_group = np.where(sDCG_is_appstore, 'App Store', removed_url_encoding_loc['sessionDefaultChannelGroup'])

    # # Prevent duplicate insertion error by deleting col. that may already be present due to running the WHOLE program previously
    # if 'channel_group' in removed_url_encoding_loc.columns:
    #     removed_url_encoding_loc.drop(columns='channel_group', inplace=True)

    # insert the new column, 'channel_group' next to original col, sDCG
    loc = removed_url_encoding_loc.columns.get_loc('sessionDefaultChannelGroup')
    removed_url_encoding_loc.insert(loc=loc + 1, column='channel_group', value=channel_group)

    # Update new column, 'channel_group' to dtype 'category' using an imported dictionary
    removed_url_encoding_loc['channel_group']= removed_url_encoding_loc['channel_group'].astype(dtype_dct['channel_group'])

    return removed_url_encoding_loc


def fix_surface_type_dupe(new_category_loc):
    # duplicate categories in surface_type for 'app detail' vs. 'app_detail',
    new_category_loc['surface_type'].unique()

    # replace space with underscore to combine duplicate into a single category: 'app_details'
    new_category_loc['surface_type'] = new_category_loc['surface_type'].replace('app details', 'app_details')

    return new_category_loc


# Surface_type has category "Unassigned"
# Assign these records to the correct  where data is available
# Delete Unassigned records when there's not enough data to assign record to

def channel_group_assign_unassigned(fixed_dupe_loc):

    # boolean of  listed as 'Unassigned'
    ts_unassigned = fixed_dupe_loc['channel_group'] == 'Unassigned'

    # boolean of surface_type not nan
    st_string_nan = fixed_dupe_loc['surface_type'].notnull()

    # bool array: if lppqs contains app name
    lppqs_regex = fixed_dupe_loc['LandingPagePlusQueryString'].str.contains(r'(/AnonymizedApp-low-stock-counter)', regex=True,
                                                                flags=re.I)

    # Where  is 'Unassigned' & surface_type is not nan &  = 'App Store'
    u1 = np.where((ts_unassigned == True) & (st_string_nan == True), 'App Store', fixed_dupe_loc['channel_group'])

    #  Where  is 'Unassigned' & surface_type is nan & lppqs contains the app name,  = 'Direct'
    fixed_dupe_loc['channel_group'] = np.where((ts_unassigned == True) & (st_string_nan == False) & (lppqs_regex == True),
                                    'Direct', u1)

    unassigned_no_data = fixed_dupe_loc.query('channel_group == "Unassigned"').index

    fixed_dupe_loc= fixed_dupe_loc.drop(index=unassigned_no_data)

    return fixed_dupe_loc