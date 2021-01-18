# generate a csv of sp500 stocks

import pandas as pd

sp500 = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')

sp500[0].to_csv('sp500_list.csv')