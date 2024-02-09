import pandas as pd
import re

from global_structures import dtype_dct

def create_df(api_re_loc):

    # Initialize empty lists to hold dimension and metric data
    d = []

    m = []

    # Count the number of dimensions and metrics in the API response
    dim_qty = len(api_re_loc.dimension_headers)
    metric_qty = len(api_re_loc.metric_headers)

    # Loop through each row in the API response object
    for row in api_re_loc.rows:

        # Create a dictionary for dimensions in the current row
        # Key: Dimension name, Value: Dimension value
        d_dct = {api_re_loc.dimension_headers[dim_index_pos].name: row.dimension_values[dim_index_pos].value
                 for dim_index_pos in range(dim_qty)}

        # Create a dictionary for metrics in the current row
        # Key: Metric name, Value: Metric value
        m_dct = {api_re_loc.metric_headers[metric_index_pos].name: row.metric_values[metric_index_pos].value
                 for metric_index_pos in range(metric_qty)}

        # Append the dictionaries to their respective lists
        d.append(d_dct)
        m.append(m_dct)

    # Combine the dimension and metric data into a single DataFrame
    df1 = pd.concat(objs=(pd.DataFrame(d), pd.DataFrame(m)), axis=1)

    # lowercase lPPQS 
    df1['landingPagePlusQueryString'] = df1['landingPagePlusQueryString'].str.lower()

    
    # assign efficient dtypes early on to reduce memory and processing overhead
    for col in df1.columns:
        # for each col in df1, assign the dtype using the dtype_dct
        df1[col] = df1[col].astype(dtype_dct[col])

    # only retain the date component of the timestamp in that you don't receive a time signature from the GA4 API
    df1['date'] = pd.to_datetime(df1['date'], format = '%Y/%m/%d').dt.date


    return(df1)

