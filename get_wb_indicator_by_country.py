import wbdata
import datetime
import pandas as pd
import numpy as np


def get_latest_wb_indicator_by_country(name: str, indicator: str):

    # Get raw data
    date = (datetime.datetime(2016, 1, 1), datetime.datetime(2016, 1, 1)) # hwo to automatically select latest date?
    raw_data = wbdata.get_data(indicator=indicator, data_date=date)

    # Get country and arrivals
    countries = []
    value = []
    for x in raw_data:
        countries.append(x['country']['value'])
        arrivals = x['value']
        if arrivals is None:
            arrivals = np.nan
        value.append(arrivals)

    # Store as pandas data frame
    data = {"country": countries, name: value}
    df = pd.DataFrame(data)

    return df


# # Example:
# population = get_latest_wb_indicator_by_country('SP.POP.TOTL', 'pop')
# print(population[:5])