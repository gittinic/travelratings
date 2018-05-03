import sys

from data_visualization import bar_plot_score, group_bar_plot, stacked_bar_plot_total_score, country_pie_chart
from tabulate import tabulate
import pandas as pd

# Global variables
from travelratings.data_visualization import score_plot_trisurf
from travelratings.flight_price_calc import getData

dict = {'1':'Affordability', '2':'Safety', '3':'Tourism'}
feat = pd.read_excel('features.xlsx', sheet_name='Features', header=0)
flight = pd.read_excel('data.xlsx', sheet_name='flight_clean', header=0)


def menu():
    """
    Menu -- Application start
    :return: according function
    """
    while(True):
        print('===========================================')
        print('Welcome to tripRatings. Here is our menu: ')
        print('1. Show bar plots')
        print('2. Show countries with top score')
        print('3. Show results by countries')
        print('4. Show country rankings')
        print('5. Check flight price by countries')
        print('6. show all indices for one country')
        print('7. statistic analysis')
        print('8. quit')
        print('Input numbers from 1 to 8...')
        x = input()
        choose(x)
        print('==========================================')
    return

def choose(x):
    """
       Choose one function to execute
       Arguments:
           x {String} -- choice

       Returns:
           function -- provided functions in the app
    """
    switcher = {
        '1': show_score_barplot,
        '2': show_stack_barplot,
        '3': show_result_country,
        '4': show_ranking_country,
        '5': show_flight_price,
        '6': show_country_pie_chart,
        '7': show_3d_chart,
        '8': quit
    }
    # Get the function from switcher dictionary
    func = switcher.get(x, lambda: print("Invalid input. Please try again."))
    # Execute the function
    func()

def show_3d_chart():
    score_plot_trisurf()
    return

def show_country_pie_chart():
    """
    Show pie chart for all indices of a country
    :return: 
    """
    print('Input the country name to check: ')
    country = input()
    country_pie_chart(country)
    return


def show_stack_barplot():
    """
    Show stack chart for scores of top countries
    :return:
    """
    print('How many top countries you want to retrive, from 1 to 30?')
    top = int(input())
    stacked_bar_plot_total_score(top)
    return


def show_score_barplot():
    """
    Show bar chart for scores of Affordability, Safety or Tourism
    :return:
    """
    try:
        print('Which score are you looking at, type 1, 2 or 3')
        print('1. Affordability')
        print('2. Safety')
        print('3. Tourism')
        scoreIdx = str(input())
        score = dict.get(scoreIdx)
        print('How many top countries you want to retrive, from 1 to 30?')
        top = int(input())
        bar_plot_score(score, top)
    except ValueError:
        print('Invalid input. Please try again')
    return


def print_results(country):
    """
    Print tables showing all data about one country
    :param country: country input by the user
    :return:
    """
    row = feat[feat['Country']==country]
    data = [
        [row['Country'], row['Affordability'], row['Safety'], row['Tourism'], row['Total'], row['Rank']],
           ]
    headers = ['Country', 'Affordability', 'Safety', 'Tourism', 'Total', 'Rank']
    print(tabulate(data, headers=headers, tablefmt='orgtbl', numalign="decimal", stralign="right", floatfmt=".2f"))


def show_result_country():
    """
    call print_results to show tables with all data about one country
    :return:
    """
    try:
        print('Which country are you interested in?')
        print('Type the country name: ')
        country = input()
        print_results(country)
        print('Showing result for one country above')
    except:
        print('Invalid input. Please try again')
    return


def print_rank(rank):
    """
    print top rank countries in a table
    :param rank: rank input by the user
    :return:
    """
    # Sort and subset data
    rank = int(rank)
    feat_sort = feat.sort_values(by=['Rank'], ascending=False)
    feat_subset = feat_sort[:rank]
    data = [
        [feat_subset['Country']]
           ]
    headers = ['Country']
    print(tabulate(data, headers=headers, tablefmt='orgtbl', numalign="decimal", stralign="right", floatfmt=".2f"))
    return


def show_ranking_country():
    """
    call print_rank
    :return:
    """
    print('Which rank are you looking for?')
    print('Type a number x from 1 to 74 to get the top x countries: ')
    rank = input()
    print_rank(rank)
    return


def show_plot_country():
    print('Showing top 5 countries')
    group_bar_plot()
    return


def print_flight(dest):
    """
    Print flight prices to the destination
    :param dest: destination input by the user
    :return:
    """
    price = flight[flight['country']==dest]
    data = [
        [price['country'], price['flight_price']]
    ]
    headers = ['Country', 'Price']
    print(tabulate(data, headers=headers, tablefmt='orgtbl', numalign="decimal", stralign="right", floatfmt=".2f"))
    return


def show_flight_price():
    """
    call print_flight
    :return:
    """
    print('Type your origin country: ')
    originC = input()
    print('Type your destination country: ')
    destC = input()
    print('Type your departure date(format: 2018-06-25): ')
    depdt = input()
    print('Type your return date(format: 2018-06-25): ')
    rtndt = input()
    print('loading...')
    print(getData(originC, destC, depdt, rtndt))
    # print_flight(dest)
    return


def quit():
    """
    quit the program
    :return:
    """
    print('Type y to quit: ')
    y = input()
    if y == y:
        sys.exit()
    return

menu()
