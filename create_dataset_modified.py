import pandas as pd
from functools import reduce

import get_cost_of_living_data as get_col
import get_attack_on_civilians as get_aoc
import get_wb_indicator_by_country as get_wbi
import amadeus as get_flight
import wbdata


wbdata.get_source()
# GET DATA

# Get cost of living
col = get_col.get_cost_of_living_data()

# Get attack on civilians
aoc = get_aoc.get_attack_on_civilians()

# Get population
pop = get_wbi.get_latest_wb_indicator_by_country("population", "SP.POP.TOTL")

# Get tourism
tourism = get_wbi.get_latest_wb_indicator_by_country("tourism", "ST.INT.ARVL")

# Get flight price
flight = get_flight.getData()

# CLEAN DATA

# aoc: Remove country code column in attack on civilians (was only used for retrieving country names)
aoc_clean = aoc.drop('country_code', axis=1)
aoc_clean = aoc_clean[['country', 'attacks']]

# pop: drop NAs
pop_clean = pop.dropna(axis=0, how='any')

# tourism: drop NAs
tourism_clean = tourism.dropna(axis=0, how='any')

# flights: drop price = '-1'
flight_clean = flight[flight.priceList != '-1']


# MERGE DATA

# Combine to single data frame
dfs = [col, aoc_clean, pop, tourism, flight]

# Merge: note that regions and country clusters in world bank data are removed by merge
merged = reduce(lambda left, right: pd.merge(left, right, on='country'), dfs)

# Drop NAs
merged = merged.dropna(axis=0, how='any')

# Set order
merged = merged[['country', 'cost_of_living', 'attacks', 'population', 'tourism', 'flight']]


# CREATE EXCEL

# Cover sheet
files = ['col_raw', 'aoc_raw', 'pop_raw', 'tourism_raw', 'flight_raw',
         'col_clean', 'aoc_clean', 'pop_clean', 'tourism_clean', 'flight_clean',
         'merged']
description = ['Raw data of cost of living index by country (Source: Numbeo)',
               'Raw data of attacks on civilians by country (Source: GDELT)',
               'Raw data of total population by country (Source: World Bank)',
               'Raw data of arriving tourists by country (Source: World Bank)',
               'Raw data of flights price by country (Source: Amadeus)',
               'Cleaned cost of living data --> cost_of_living',
               'Cleaned attacks on civilians data --> variable attacks',
               'Cleaned total population data --> population',
               'Cleaned arriving tourists data --> tourism',
               'Cleaned flight price data --> flight',
               'Merged data with columns: country, cost_of_living, attacks, population, tourism and flight']
cover = pd.DataFrame({'files': files, 'description': description})
cover = cover[['files', 'description']]

# Write data frames
writer = pd.ExcelWriter('data.xlsx')
cover.to_excel(writer,'cover', index=False)
col.to_excel(writer,'col_raw', index=False)
aoc.to_excel(writer,'aoc_raw', index=False)
pop.to_excel(writer, 'pop_raw', index=False)
tourism.to_excel(writer, 'tourism_raw', index=False)
flight.to_excel(writer, 'flight_raw', index=False)
col.to_excel(writer,'col_clean', index=False)
aoc_clean.to_excel(writer,'aoc_clean', index=False)
pop_clean.to_excel(writer, 'pop_clean', index=False)
tourism_clean.to_excel(writer, 'tourism_clean', index=False)
flight_clean.to_excel(writer, 'flight_clean', index=False)
merged.to_excel(writer, 'merged', index=False)
writer.save()


