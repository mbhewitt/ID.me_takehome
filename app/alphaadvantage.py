import requests
from statistics import mean
import logging

logging.basicConfig(encoding='utf-8', level=logging.INFO)
#TODO: Set logging level on command line or config file


# Retrieves and averages the closing price of symbol for previous X days
def getCloseDataAvg(symbol,days):
    stockData={}
    priceList=[]
    #TODO: move APIKEY out to command line or config file because it is a credential.
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

#TODO: move what symbol and number of days to command line
getCloseDataAvg(symbol="GOOG",days=5)



# https://www.alphavantage.co/documentation/
# get APIkey https://www.alphavantage.co/support/#api-key
# Retrieved JSON structure

"""
{
    "Meta Data": {
        "1. Information": "Daily Time Series with Splits and Dividend Events",
        "2. Symbol": "GOOG",
        "3. Last Refreshed": "2023-02-27",
        "4. Output Size": "Compact",
        "5. Time Zone": "US/Eastern"
    },
    "Time Series (Daily)": {
        "2023-02-27": {
            "1. open": "90.09",
            "2. high": "90.4499",
            "3. low": "89.61",
            "4. close": "90.1",
            "5. adjusted close": "90.1",
            "6. volume": "22724262",
            "7. dividend amount": "0.0000",
            "8. split coefficient": "1.0"
        },
        ...
    }
}
"""
