import pandas as pd
from functools import reduce
import numpy as np

import numbeo
import worldbank
import gdelt

# GET DATA

# Get cost of living
col = numbeo.get_cost_of_living_data()

# Get attack on civilians
aoc = gdelt.get_attack_on_civilians()

# Get population
pop = worldbank.get_latest_wb_indicator_by_country("population", "SP.POP.TOTL")

# Get tourism
tourism = worldbank.get_latest_wb_indicator_by_country("tourism", "ST.INT.ARVL")


# CLEAN DATA

# aoc: Remove country code column in attack on civilians (was only used for retrieving country names)
aoc_clean = aoc.drop('country_code', axis=1)
aoc_clean = aoc_clean[['country', 'attacks']]

# pop: drop NAs
pop_clean = pop.dropna(axis=0, how='any')

# tourism: drop NAs and convert to numeric
tourism_clean = tourism.dropna(axis=0, how='any')
tourism_clean['tourism'] = pd.to_numeric(tourism_clean['tourism'])


# MERGE DATA

# Combine to single data frame
dfs = [col, aoc_clean, pop_clean, tourism_clean]

# Merge: note that regions and country clusters in world bank data are removed by merge
merged = reduce(lambda left, right: pd.merge(left, right, on='country'), dfs)

# Drop NAs
merged = merged.dropna(axis=0, how='any')

# Set order
merged = merged[['country', 'cost_of_living', 'attacks', 'population', 'tourism']]


# CREATE EXCEL

# Cover sheet
files = ['col_raw', 'aoc_raw', 'pop_raw', 'tourism_raw',
         'col_clean', 'aoc_clean', 'pop_clean', 'tourism_clean',
         'merged', '', 'Note 1:', "Note 2:"]
description = ['Raw data of cost of living index by country (Source: Numbeo)',
               'Raw data of attacks on civilians by country in 2018 (Source: GDELT Project)',
               'Raw data of total population by country, 2016 (Source: World Bank)',
               'Raw data of arriving tourists by country, 2016 (Source: World Bank)',
               'Cleaned cost of living data --> cost_of_living',
               'Cleaned attacks on civilians data --> variable attacks',
               'Cleaned total population data --> population',
               'Cleaned arriving tourists data --> tourism',
               'Merged data with columns: country, cost_of_living, attacks, population, tourism',
               '',
               'Some rows in the merged set may be lost due to NAs or because the matching key slightly differs (may be improved in the future).',
               'Flight price data will be queried via amadeus.py in the application once the user has chosen a destination based on the above data.']
cover = pd.DataFrame({'files': files, 'description': description})
cover = cover[['files', 'description']]

# Write data frames
writer = pd.ExcelWriter('data.xlsx')
cover.to_excel(writer,'cover', index=False)
col.to_excel(writer,'col_raw', index=False)
aoc.to_excel(writer,'aoc_raw', index=False)
pop.to_excel(writer, 'pop_raw', index=False)
tourism.to_excel(writer, 'tourism_raw', index=False)
col.to_excel(writer,'col_clean', index=False)
aoc_clean.to_excel(writer,'aoc_clean', index=False)
pop_clean.to_excel(writer, 'pop_clean', index=False)
tourism_clean.to_excel(writer, 'tourism_clean', index=False)
merged.to_excel(writer, 'merged', index=False)
writer.save()