import pandas as pd
import numpy as np
from global_structures import dtype_dct

def misc_cleaning(assigned_channel_group_loc):

    # determine which columns have the dtype string, object, or category
    string_cols = [col for col in assigned_channel_group_loc.columns if
                   assigned_channel_group_loc[col].dtype in ['O', 'string', 'category']]

    # replace 'nan' with np.nan, save the updated column in-place
    for col in string_cols:
        assigned_channel_group_loc[col] = assigned_channel_group_loc[col].replace('nan', np.nan)

    # Update 'channel_group' to dtype 'category' using an imported dictionary
    assigned_channel_group_loc['channel_group'] =  assigned_channel_group_loc['channel_group'].astype(dtype_dct['channel_group'])

    return assigned_channel_group_loc