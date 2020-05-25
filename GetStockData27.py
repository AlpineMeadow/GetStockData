#! /usr/bin/env python3

#A program to get stock data.

#Gather our code in a main() function.
def main() :
    import sys
    sys.path.append('/home/jdw/UM2020Spring/M567/Functions/')
    import StockFunctions as sf


    #First we get some data.  This function returns an array of times and prices.
    #First set the length of time to get.
    numHours = 6
    numSec = numHours * 360
    sleepTime = 10

    #The name of the stock we are looking at.
    tag = 'tsla'  #Tesla
    data = sf.query(numSec, sleepTime, tag)

    
# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
