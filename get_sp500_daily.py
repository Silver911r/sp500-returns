import yfinance as yf
import csv
import plotly.express as px
from datetime import date
from scipy import stats

today = date.today()

#dictionary of stats by stock sybmol
stock_stat = {}

#open symobl csv
with open('sp500_list.csv', newline='') as f:
    reader = csv.reader(f)
    data = list(reader)

for stock in data:
    print('fetching ', stock, ' history')

    stock = stock[1]
    ticker = yf.Ticker(stock)
    stock_df = ticker.history(period='1y')


    #calculate the return column
    print('Calculate Returns for ', stock)
    stock_df['Return'] = stock_df['Close'].pct_change()
    stock_df.dropna(inplace=True)

    #save csv of data
    print('Save csv ', stock)
    stock_df.to_csv(f'data/{stock}.csv')

    #create and save histogram to the histogram folder
    print('Create histogram for ', stock)
    fig = px.histogram(stock_df, 
                        x="Return",
                        title=stock + ' Daily Return',
                        log_y=True,
                        marginal="rug")
    fig.write_html("histograms/" + stock + "-histogram-" + today.isoformat() + ".html")

    #create list of the returns
    returns = list(stock_df['Return'])

    #must have more than 8 returns to calculate the results
    print('Calculate stats for ', stock)
    if len(returns) > 8:
        stat, p = stats.normaltest(returns)

        #descriptions of stats
        desc = stats.describe(returns)
        #save stats to dictionary
        stock_stat[stock] = ['stat',stat], ['p',p], ['desc',desc]


#save dictionary to csv
print('Save stats')
with open('sp500_stats.csv', 'w') as f:
    for key in stock_stat.keys():
        f.write("%s,%s\n"%(key,stock_stat[key]))