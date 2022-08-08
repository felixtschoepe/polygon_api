#%% Import Modules

# zuerst die nötigen Librarys laden
# pip OR conda install
# pip install polygon-api-client
# pip install plotly


from polygon import RESTClient
import datetime as dt
import pandas as pd
import plotly.graph_objects as go
from plotly.offline import plot
#from get_polygon_data import POLYGON_API_KEY
import plotly.express as px
import time


# %%  
# API Key einbinden

polygonAPIkey = '63g5kApL_17IUs73a4FWukvDBdlZzJCi'
client = RESTClient(polygonAPIkey) 

# api key from config
#polygonAPIkey = '63g5kApL_17IUs73a4FWukvDBdlZzJCi'

# create client and authenticate w/ API key // rate limit 5 requests per min
client = RESTClient(polygonAPIkey) # api_key is used

# %%
# Ticker von Polygon abholen
tickerlist = client.list_tickers(ticker = None, exchange = 'XNYS', limit = 1000)
tickerlist = pd.DataFrame(tickerlist)
print(tickerlist)

# %%
tickerlisttype = tickerlist[tickerlist.type == 'CS']
tickerlisttype = pd.DataFrame(tickerlisttype)
print(tickerlisttype)


# %%
# für Stocks 
tickerNames = ['AAPL','AMGN','BTI','CSCO','DIS','JNJ','KO','MAIN','MCD','MMM','MO','MSFT','NFLX',
            'NKE','O','OHI','PEP','PG','SBUX','SKT','T','TXN','UL','V']
#for c in client.list_tickers(ticker=None, limit=1000):
#    tickerNames.append(c)
#print(tickerNames)


# für Optionen funktionsfähig
#contractNames = []
#for c in client.list_options_contracts(underlying_ticker = 'AAPL', limit = 1000):
#    contractNames.append(c)
#print(contractNames)

# %%
# Durchlauf in einer Schleife
tickers = tickerlisttype['ticker']
#tickers = ['AAPL','AMGN','BTI','CSCO','DIS','JNJ','KO','MAIN','MCD','MMM','MO','MSFT','NFLX',
#            'NKE','O','OHI','PEP','PG','SBUX','SKT','T','TXN','UL','V']

tickerslaenge = len(tickers)
tickerslaenge1 = tickerslaenge / 5

counterschleife = 0
warteschleife = 1
print('Es geht los: %s' % time.ctime())

for ticker in tickers:
    stockdata = client.get_aggs(ticker = ticker,
                                multiplier=1,
                                timespan='day',
                                from_ = '2020-09-01',
                                to='2022-08-07')
    stockdataframe = pd.DataFrame(stockdata)
    stockdataframe['Date'] = stockdataframe['timestamp'].apply(
                                lambda x: pd.to_datetime(x*1000000)
    )
    stockdataframe = stockdataframe.set_index('Date')
    stockdataframe.to_csv('data/datasets/{}.csv'.format(ticker), index=True, sep=',')
    msg = ('CSV-Datei für ' + ticker + ' gespeichert.')
    print(msg)

    divdata = client.list_dividends(ticker=ticker,
                                    limit=1000)
    divdata = pd.DataFrame(divdata)
    divdata.to_csv('data/divs/{}.csv'.format(ticker), index=False, sep=',')
    divmsg = ('Dividendendaten für ' + ticker + ' gespeichert.')
    print(divmsg)
    counterschleife +=1
    if counterschleife == 5:
        wartemsg = ('Warteschleife Nr.: ' + str(warteschleife) + ' von ' + str(tickerslaenge1) + ' .')
        print(wartemsg)
        warteschleife += 1
        counterschleife = 0
        time.sleep(60)
print('Aktualisierung fertig: %s' % time.ctime())    

# %% bekomme den Ticker für die Suche

# to view individual contract gneeral data
#contractData = contractNames[398]

# get options ticker
#optionsTicker = contractData.ticker
#print(optionsTicker)

#%% 
# hole die Werte (Kurse, Dividenden) ab und sichere sie als CSV
activeTicker = 'V'
# daily options price bars
dailyStockData = client.get_aggs(ticker = activeTicker,
                                multiplier = 1,
                                timespan = 'day',
                                from_ = '2020-09-01',
                                to = '2022-08-06',)

StockDataFrame = pd.DataFrame(dailyStockData)
# create Date column
StockDataFrame['Date'] = StockDataFrame['timestamp'].apply(
                            lambda x: pd.to_datetime(x*1000000)
)
StockDataFrame = StockDataFrame.set_index('Date')
# Speichern der Daten als CSV-Datei
StockDataFrame.to_csv('data/datasets/{}.csv'.format(activeTicker), index=True, sep=',')
msg = ('CSV-Datei für ' + activeTicker + ' gespeichert.')
print(msg)

# Hier für Dividenden
DivData = client.list_dividends(ticker=activeTicker,
                                limit=1000)

DivData = pd.DataFrame(DivData)

DivData.to_csv('data/divs/{}.csv'.format(activeTicker), index=False, sep=',')
divmsg = ('Dividenden-Datei für ' + activeTicker + ' gespeichert.')
print(divmsg)
#print(dailyStockData)

# %%
#list of polygon OptionsContract objects to DataFrame
# StockDataFrame = pd.DataFrame(dailyStockData)
# #print(StockDataFrame)

# # create Date column
# StockDataFrame['Date'] = StockDataFrame['timestamp'].apply(
#                             lambda x: pd.to_datetime(x*1000000)
# )

# StockDataFrame = StockDataFrame.set_index('Date')

# # Speichern der Daten als CSV-Datei
# StockDataFrame.to_csv('data/datasets/{}.csv'.format(activeTicker), index=True, sep=',')
# msg = ('CSV-Datei für ' + activeTicker + ' gespeichert.')
# print(msg)

#print(StockDataFrame)


# %%
# generate plotly figure
fig = go.Figure(data=[go.Candlestick(x=StockDataFrame.index,
    open=StockDataFrame['open'],
    high=StockDataFrame['high'],
    low=StockDataFrame['low'],
    close=StockDataFrame['close'])])

# open figure in browser
plot(fig, auto_open=True)

# %% hole Dividenden
# DivData = client.list_dividends(ticker=activeTicker,
#                                 limit=1000)

# DivData = pd.DataFrame(DivData)

#print(DivData)

# gebe die Überschriten aus zur Anzeige
for column in DivData:
    print(column)

# %% Linenchart für Dividenden
divfig = px.line(x=DivData['pay_date'],
                y=DivData['cash_amount'])
plot(divfig, auto_open=True)

# %% Barchart für Dividenden

divbarfig = px.bar(DivData, x=DivData['pay_date'], # Zahltag
                    y=DivData['cash_amount'], # Dividende
                    labels={'pay_date': 'Datum', 'cash_amount': 'US-Dollar'}) # Achsenbeschriftung
plot(divbarfig, auto_open=True) # Öffne die Grafik im Browser
# %%
