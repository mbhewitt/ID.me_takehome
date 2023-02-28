import requests
from statistics import mean
import logging

logging.basicConfig(encoding='utf-8', level=logging.INFO)

def getCloseDataAvg(symbol,days):
    stockData={}
    priceList=[]
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey=2PC8C9EVNUKMJRCK'

    try:
       r = requests.get(url)
       stockData = r.json()
    except requests.exceptions.ConnectionError:
        logging.error(f"Could not retrieve data from {url}.")
        exit()

    if("Time Series (Daily)" not in stockData):
        logging.error(f"Time Series data not found in retrieved json. Is {symbol} correct?")
        exit()

    timeseries=stockData["Time Series (Daily)"]
    daysInTimeseries=len(timeseries)

    if(daysInTimeseries<days):
        logging.warning(f"Note: Requested days({days}) is larger than available days ({daysInTimeseries}).")

    datesOfInterest=list(timeseries)[:days] #trim list to just the previous X days

    for date in datesOfInterest:
        daysData=timeseries[date]
        closingPrice=daysData["4. close"]
        priceList.append(float(closingPrice))
        logging.info(f"Closing price for {symbol} on {date} ${closingPrice}")

    avgStockPrice=mean(priceList)
    print(f"{days} day average closing {symbol} Price ${avgStockPrice}")

getCloseDataAvg("GOOG",5)
