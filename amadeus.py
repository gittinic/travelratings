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
    row = df_airport.loc[df_airport['Country'].str.lower() == country]
    return row['Code']

# get all countries needed
def getCountries():
    with open('countries', 'r') as col:
        lines = col.read().splitlines()
    countries = [x.lower() for x in lines]
    return countries
# get key
def readKey():
    with open('key.txt', 'r') as file:
        key = file.readline()
    return key

# get flight price data from Amadeus API
def getData():
    priceList = []
    orgList = []
    destList = []
    apiKey = readKey()
    # set query parameter
    origin = ['JFK']
    departure_date = ['2018-07-15']
    desination = []
    
    # read all countries from txt
    countries = getCountries()
    for country in countries:
        list = find_airportCode_for_country(country).tolist()
        while '\\N' in list: list.remove('\\N')
        if len(list) > 0:
            code = list[0]
            desination.append(code)
            
    output = open("out.csv", "w")

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}

    # Make a get request to get the latest price
    for org in origin:
        for dest in desination:
            if org != dest:
                for depdt in departure_date:
                    
                    # write the corresponding destination country
                    desCountry = find_country_for_airport_code(dest)
                    output.write(desCountry + ',')
                    destList.append(desCountry)
                    
                    # construct the url with encoding
                    start = "https://apiconsole-prod.apigee.net/smartdocs/v1/sendrequest?targeturl=https%3A%2F%2Fapi.sandbox.amadeus.com%2Fv1.2%2F"

                    partUrl = "flights/low-fare-search?" \
                              "apikey=" + apiKey + \
                              "&origin=" + org + \
                              "&destination=" + dest + \
                              "&departure_date=" + depdt + \
                              "&_=1523980626850"
                    url = start + urllib.parse.quote_plus(partUrl)
                    print(url)

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
                    output.write(price + '\n')
                    print(desCountry + ',' + price + '\n')
    output.close()
    # build data frame
    data = {"destination": destList, "price": priceList}
    df_label = pd.DataFrame(data)
    return df_label

def main():
    getData()
    # test()
if __name__ == '__main__':
    main()