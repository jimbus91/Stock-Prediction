import datetime
import mplfinance
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from yahoofinancials import YahooFinancials
from sklearn.linear_model import LinearRegression

stock=input("Enter the stock ticker symbol: ")

highs=[]
lows=[]
opens=[]
closes=[]

# Get the current date and date 10 years ago
current_date = datetime.datetime.now()
ten_years_ago_date = current_date - datetime.timedelta(days=365*10)

yahoo_financials = YahooFinancials(str(stock))
stats=(yahoo_financials.get_historical_price_data(ten_years_ago_date.strftime("%Y-%m-%d"), current_date.strftime("%Y-%m-%d"), "daily"))

i = 0

# Iterating through the prices of the stock and adding the high,low,open and close prices in respective lists
for date in stats[str(stock)]["prices"]:
    if i == 0:
        i +=1
        continue
    highs.append(date['high'])
    lows.append(date['low'])
    opens.append(date['open'])
    closes.append(date['close'])
    i += 1
    print("No. of data pts:",i)
    total = []
    totalopens=[]
    for j in range(4):
        opens.append(0)

# Appending the data in the list total
for i in range(i-1):
    total.append([opens[i],lows[i],highs[i], closes[i]])

# Function to predict stock prices
def Predictor(lst,months):
    total_training = lst[0:i-months]
    total_validation = lst[i-months:]

    # Converting data into dataframe
    df = pd.DataFrame(total_training, dtype=float)
    XTrain = df.iloc[:, :-1]
    yTrain = df.iloc[:, [-1]]

    # Creating linear regression model
    clf = LinearRegression()
    clf.fit(XTrain, yTrain)

    print("\n\n")

    # Splitting data into validation data
    dfP = pd.DataFrame(total_validation, dtype=float)
    XValidation = dfP.iloc[:, :-1]
    YValidation = dfP.iloc[:, [-1]]

    print("\n\nPrediction")
    YPrediction = clf.predict(XValidation)

    # Printing original and predicted data
    print("\nOriginal")
    print(YValidation)

    print("\nPredicted")
    print(YPrediction)

Predictor(total,1)