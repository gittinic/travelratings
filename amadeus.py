import requests
import json
import urllib.parse


def getData():
    origin = ['JFK', 'PEK', 'LON', 'HEL', 'CDG']
    # origin = ['JFK']
    detination = ['LON', 'PEK', 'BER', 'CDG', 'HEL']
    # detination = ['LON']
    departure_date = ['2018-01-15', '2018-02-15', '2018-03-15', '2018-04-15', '2018-05-15', '2018-06-15', '2018-07-15', '2018-08-15', '2018-09-15', '2018-10-15', '2018-11-15', '2018-12-15']
    # departure_date = ['2018-11-15']
    output = open("out.csv", "w")

    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'}

    # Make a get request to get the latest price
    for org in origin:
        for dest in detination:
            if org != dest:
                for depdt in departure_date:
                    start = "https://apiconsole-prod.apigee.net/smartdocs/v1/sendrequest?targeturl=https%3A%2F%2Fapi.sandbox.amadeus.com%2Fv1.2%2F"

                    partUrl = "flights/low-fare-search?" \
                              "apikey=cdfc2noTw8v5Rp3gsGPA8ZgjQGWvtrRl" \
                              "&origin=" + org + \
                              "&destination=" + dest + \
                              "&departure_date=2018-05-15&_=1523980626850"
                    url = start + urllib.parse.quote_plus(partUrl)
                    print(url)
                    output.write(org + ',' + dest + ',' + depdt + ',')
                    response = requests.get(url, headers=headers)
                    # Print the status code of the response.
                    print(response.status_code)
                    text = response.text
                    jsonData = json.loads(text)
                    responseContent = jsonData['responseContent']
                    decoded = urllib.parse.unquote(responseContent)
                    print(decoded)
                    decodedJson = json.loads(decoded)
                    price = decodedJson['results'][0]['fare']['total_price']
                    output.write(price + '\n')
                    print(org + ',' + dest + ',' + depdt + ',' + price + '\n')
    output.close()

def test():
    start = "https://apiconsole-prod.apigee.net/smartdocs/v1/sendrequest?targeturl=https%3A%2F%2Fapi.sandbox.amadeus.com%2Fv1.2%2F"
    partUrl = "flights/low-fare-search?origin=IST&destination=BOS&departure_date=2018-10-15&return_date=2018-10-21&number_of_results=3&apikey=cdfc2noTw8v5Rp3gsGPA8ZgjQGWvtrRl"
    url = start + urllib.parse.quote_plus(partUrl)
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.90 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    text = (response.text)
    jsonData = json.loads(text)
    responseContent = jsonData['responseContent']
    test = responseContent
    decoded = urllib.parse.unquote(test)
    print(decoded)
    decodedJson = json.loads(decoded)
    itineraries = decodedJson['results'][0]['fare']['total_price']
    print(itineraries)

def main():
    getData()
    # test()
if __name__ == '__main__':
    main()