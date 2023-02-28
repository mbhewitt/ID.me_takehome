import requests
from statistics import mean

def getCloseDataAvg(symbol,days):
    stockData={}
    priceList=[]
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey=2PC8C9EVNUKMJRCK'
    try:
       r = requests.get(url)
       stockData = r.json()
    except requests.exceptions.ConnectionError:
        print(f"Could not retrieve data from {url}.")
        exit()
    if("Time Series (Daily)" not in stockData):
        print("Time Series data not found in retrieved json.")
        exit()
    timeseries=stockData["Time Series (Daily)"]
    daysInTimeseries=len(timeseries)
    if(daysInTimeseries<days):
        print(f"Note: Requested days({days}) is larger than available days ({daysInTimeseries}).")
    datesOfInterest=list(timeseries)[:days]
    for date in datesOfInterest:
        daysData=timeseries[date]
        closingPrice=daysData["4. close"]
        priceList.append(float(closingPrice))
        print(f"Closing price for {symbol} on {date} ${closingPrice}")

    avgStockPrice=mean(priceList)
    print(f"{days} day average closing {symbol} Price ${avgStockPrice}")

getCloseDataAvg("GOOG",5)
