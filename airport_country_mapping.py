import pandas as pd


def get_airport_data():
    df = pd.read_table("airports.dat", sep=",", header=None,
                               names=['Airport', 'City', 'Country', 'Code',
                                      'X1', 'X2', 'X4', 'X5', 'X6', 'X7', 'X8', 'X9', 'X10'])
    return df


def find_country_for_airport_code(airport_code: str):
    df_airport = get_airport_data()
    row = df_airport.loc[df_airport['Code'] == airport_code]
    return row['Country']