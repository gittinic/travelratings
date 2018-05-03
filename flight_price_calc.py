'''
== About the data ==
- Source: amadeus
- Variables: flight price
- Data is retrieved via the company's API.

@author: Rui
'''


import requests
import json
import urllib.parse
import pandas as pd


# airport data stores the raw data including airport, city, country, airport code
def get_airport_data():
    df = pd.read_table("airports.dat", sep=",", header=None,
                               names=['Airport', 'City', 'Country', 'Code',
                                      'X1', 'X2', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10'])
    return df


# find corresponding country for the airport code
def find_country_for_airport_code(airport_code: str):
    df_airport = get_airport_data()
    row = df_airport.loc[df_airport['Code'] == airport_code]
    return row['Country'].tolist()[0]


# find corresponding airport code for the country
def find_airportCode_for_country(country: str):
    df_airport = get_airport_data()
    row = df_airport.loc[df_airport['Country'].str.lower() == country.lower()]
    return row['Code'].tolist()[0]


# get key
def readKey():
    with open('amadeus_api_key.txt', 'r') as file:
        key = file.readline()
    return key


# get flight price data from Amadeus API
def getData(originC, destC, depdt, rtndt):
    priceList = []
    apiKey = readKey()
    # set query parameter
    # find airport code for origin and dest
    origin = find_airportCode_for_country(originC)
    dest = find_airportCode_for_country(destC)
    print('Airport codes: ')
    print(origin + '\t' + dest)
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}

    # Make a get request to get the latest price
    # construct the url with encoding
    start = "https://apiconsole-prod.apigee.net/smartdocs/v1/sendrequest?targeturl=https%3A%2F%2Fapi.sandbox.amadeus.com%2Fv1.2%2F"

    partUrl = "flights/low-fare-search?" \
              "apikey=" + apiKey + \
              "&origin=" + origin + \
              "&destination=" + dest + \
              "&departure_date=" + depdt + \
              "&return_date=" + rtndt + \
              "&_=1523980626850"
    url = start + urllib.parse.quote_plus(partUrl)
    # print(url)

    # Print the status code of the response.
    # print(response.status_code)
    response = requests.get(url, headers=headers)

    # decode the response content and parse json to extract price
    text = response.text
    jsonData = json.loads(text)
    responseContent = jsonData['responseContent']
    decoded = urllib.parse.unquote(responseContent)
    decodedJson = json.loads(decoded)
    if 'results' in decodedJson:
        result = decodedJson['results']
        if len(result) > 0:
            price = result[0]['fare']['total_price']
    else:
        price = '-1'
    # write price
    priceList.append(price)
    print('The flight price is ' + price + '\n')
    # build data frame
    data = {"origin": origin, "destination":dest, "flight_price": priceList}
    df_label = pd.DataFrame(data)
    return price


def main():
    getData('Canada', 'Norway', '2018-06-25', '2018-07-01')

if __name__ == '__main__':
    main()
