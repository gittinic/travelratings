# About the data:
# Source Numbeo https://www.numbeo.com/cost-of-living/rankings_by_country.jsp
# International cost of living index
# Data collection via web scrap

# Imports
import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

# Request web page and get the page contents
page = requests.get('https://www.numbeo.com/cost-of-living/rankings_by_country.jsp')
page = page.content

# Use page to create a BeautifulSoup object and specify the type of parser
soup = bs(page, 'html.parser')

# Country
countries_td = soup.findAll("td", {"class": "cityOrCountryInIndicesTable"})
countries = []
for td in countries_td:
    countries.append(td.get_text())

# Cost of Living
table_rows = soup.findAll('table', {"id": "t2"})[0].tbody.findAll('tr')
cost_of_living = []
for row in table_rows:
    third_column = row.findAll('td')[2].contents
    cost_of_living.append(float(third_column[0]))

# Create pandas data frame
data = {'Country': countries, "Cost_Of_Living": cost_of_living}
df = pd.DataFrame(data)

