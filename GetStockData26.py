#! /usr/bin/env python3

#A program to get stock data.

#Gather our code in a main() function.
def main() :
    import sys
    import time
    sys.path.append('/home/jdw/UM2020Spring/M567/GetStockData/')
    import StockFunctions as gsf

    #First we get some data.  This function returns an array of times and prices.
    #First set the length of time to get.
    numHours = 6
    numSec = numHours * 360

    #The variable sleepTime is the number of seconds to sleep before getting
    #another stock price.
    sleepTime = 10

    #Let us get the data and time.
    dt = time.localtime()
    yearStr = str('{0:02d}'.format(dt.tm_year))
    monthStr = str('{0:02d}'.format(dt.tm_mon))
    dayStr = str('{0:02d}'.format(dt.tm_mday))
    hourStr = str('{0:02d}'.format(dt.tm_hour))
    minuteStr = str('{0:02d}'.format(dt.tm_min))

    dateTime = (yearStr + monthStr + dayStr + hourStr + minuteStr)

    #The name of the stock we are looking at.
    stockAbbrev = 'tgt'  #Target

    #Now get the data from the IEX server.
    data = gsf.query(numSec, sleepTime, stockAbbrev, dateTime)

    #Now plot the data.
    succeed = gsf.visualizeDailyStockPrice(data, stockAbbrev, dateTime)
     
# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
