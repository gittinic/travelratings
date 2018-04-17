# About the data:
# Source gdeltproject.org
# Attacks on civilians
# Tutorial on how to get the data:
# http://nbviewer.jupyter.org/github/JamesPHoughton/Published_Blog_Scripts/blob/master/GDELT%20Wrangler%20-%20Clean.ipynb


import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

def get_country_code_name():
    page = requests.get('https://wits.worldbank.org/wits/wits/witshelp/content/codes/country_codes.htm')
    page = page.content
    soup = bs(page, 'html.parser')

    # Country name
    names_p = soup.findAll("p", {"class": "WTN"})
    names = []
    for name in names_p:
        names.append(name.get_text().strip())

    # Country code
    codes_p = soup.findAll("p", {"class": "WTNC"}) # every second element ist the 3digit number --> remove every 2nd
    del codes_p[1::2]
    codes = []
    for code in codes_p:
        codes.append(code.get_text().strip())

    # Convert to pandas
    data = {'country_code': codes, "country_name": names}
    df_label = pd.DataFrame(data)

    return df_label


def get_attack_on_civilians():
    # SQL query for attack on civilians (event code) by country code in 2018
    query = ('''
        SELECT country_code, COUNT(*) AS attacks
        FROM (SELECT Actor2CountryCode country_code FROM [gdelt-bq:gdeltv2.events] WHERE YEAR=2018 AND EventCode="170")
        GROUP BY country_code''')

    # Run query and convert to panda data frame
    df = pd.read_gbq(query, "gdelt-201419")

    # Assign country name
    df_label = get_country_code_name()
    df = pd.merge(df, df_label, on='country_code')

    return df