from data_visualization import bar_plot_score
from tabulate import tabulate
import pandas as pd

dict = {'1':'Affordability', '2':'Safety', '3':'Tourism'}
feat = pd.read_excel('features.xlsx', sheet_name='Features', header=0)
flight = pd.read_excel('data.xlsx', sheet_name='flight_clean', header=0)
quit = False

def menu():
    while(quit != True):
        print('Welcome to tripRatings. Here is our menu: ')
        print('1. Show bar plots')
        print('2. Show map')
        print('3. Show results by countries')
        print('4. Show country rankings')
        print('5. Check flight price by countries')
        print('6. Indices for one country')
        print('7. Quit')
        print('Input numbers from 1 to 7...')
        x = input()
        print(choose(x))


def show_score_barplot():
    print('Which score are you looking at')
    print('1. Affordability')
    print('2. Safety')
    print('3. Tourism')
    scoreIdx = str(input())
    score = dict.get(scoreIdx)
    print('How many top countries you want to retrive?')
    top = int(input())
    bar_plot_score(score, top)
    return

def print_results(country='Switzerland'):
    row = feat[feat['Country']==country]
    data = [
        [row['Country'], row['Affordability'], row['Safety'], row['Tourism'], row['Total'], row['Rank']],
           ]
    headers = ['Country', 'Affordability', 'Safety', 'Tourism', 'Total', 'Rank']
    print(tabulate(data, headers=headers, tablefmt='orgtbl', numalign="decimal", stralign="right", floatfmt=".2f"))

def show_result_country():
    print('Which country are you interested in?')
    print('Type the country name: ')
    country = input()
    print_results(country)
    print('Showing result for one country')
    return


def print_rank(rank):
    # Sort and subset data
    feat_sort = feat.sort_values(by=['Rank'], ascending=False)
    feat_subset = feat_sort[:rank]
    data = [
        [feat_subset['Country'], feat['Rank']]
           ]
    headers = ['Country', 'Rank']
    print(tabulate(data, headers=headers, tablefmt='orgtbl', numalign="decimal", stralign="right", floatfmt=".2f"))
    return


def show_ranking_country():
    print('Which rank are you looking for?')
    print('Type a number x from 1 to 100 to get the top x countries: ')
    rank = input()
    print_rank(rank)
    return

def show_plot_country():
    print('Which country are you looking for?')
    print('Type the country name: ')
    country = input()
    # country_plot(country)
    return


def print_flight(dest):
    price = flight[flight['country']==dest]
    data = [
        [price['country'], price['flight_price']]
    ]
    headers = ['Country', 'Price']
    print(tabulate(data, headers=headers, tablefmt='orgtbl', numalign="decimal", stralign="right", floatfmt=".2f"))
    return


def show_flight_price():
    print('Type your destination: ')
    dest = input()
    print_flight(dest)
    return

def quit():
    quit = True
    return

def choose(x):
    switcher =  {
        '1': show_score_barplot,
        '2': 'Map Here...',
        '3': show_result_country,
        '4': show_ranking_country,
        '5': show_flight_price,
        '6': show_plot_country,
        '7': quit
    }
    # Get the function from switcher dictionary
    func = switcher.get(x, lambda: "Invalid")
    # Execute the function
    func()

menu()
