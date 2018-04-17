import wbdata
import datetime
import pandas as pd


def get_latest_wb_indicator_by_country(name: str, indicator: str):

    # Get raw data
    date = (datetime.datetime(2016, 1, 1), datetime.datetime(2016, 1, 1)) # hwo to automatically select latest date?
    raw_data = wbdata.get_data(indicator=indicator, data_date=date)

    # Get country and arrivals
    countries_code = []
    countries = []
    value = []
    for x in raw_data:
        countries_code.append(x['country_code'])
        countries.append(x['country']['value'])
        value.append(x['value'])

    # Store as pandas data frame
    data = {"country": countries, name: value}
    df = pd.DataFrame(data)

    return df


# # Example:
# population = get_latest_wb_indicator_by_country('SP.POP.TOTL', 'pop')
# print(population[:5])