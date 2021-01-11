#! /usr/bin/env python3

#A program to download stock data from the server, save it to a file and plot the
#time series.

from collections import defaultdict
#Set StD to a default dictionary that contains lists for the values.
StD = defaultdict(list)

StD = {'21CenturyFox': ['foxa', ['Entertainment']],
       '3M': ['mmm', ['Manufacturing', 'Technology']],
       'Amazon': ['amzn', ['Retail', 'Technology']],
       'AmericanExpress' : ['axp', ['Finance']],
       'Apple': ['aapl', ['Technology', 'Retail']],
       'ATT': ['t', ['Communications', 'Technology']],
       'Boeing': ['ba', ['Manufacturing', 'Technology']],
       'BritishPetroleum': ['bp', ['Energy']],
       'Charter': ['chtr', ['Communications']],
       'Disney': ['dis', ['Entertainment']],
       'DukeEnergy': ['duk', ['Energy']],
       'ExxonMobile': ['xom', ['Energy']],
       'GE': ['ge', ['Manufacturing', 'Technology']],
       'Google': ['goog', ['Technology']],
       'HomeDepot' : ['hd', ['Retail']],
       'Honda' : ['hmc', ['Manufacturing']],       
       'JPMorgan': ['jpm', ['Finance']],
       'Micron' : ['mu', ['Technology']],
       'Microsoft': ['msft', ['Technology']],
       'Netflix': ['nflx', ['Entertainment']],
       'Nike': ['nke', ['Retail']],
       'Nokia': ['nok', ['Technology', 'Retail']],
       'ProcterGamble': ['pg', ['Retail', 'Manufacturing']],
       'SouthwestGasCorp' : ['swx', ['Energy']],
       'StanleyBlackDecker': ['swk', ['Manufacturing', 'Retail']],
       'Target': ['tgt', ['Retail']],
       'Tesla': ['tsla', ['Manufacturing', 'Technology']],
       'USSteel': ['x', ['Manufacturing']],
       'Verizon': ['vz', ['Communications']]}

################################################################################

################################################################################

#Define a function that gets stock names given an stock abbreviation.
def getStockName(abbrev) :
  return list(StD.keys())[list(StD.values()).index(abbrev)]
#End of the function getStockNames.py
##################################################################################

##################################################################################

#Define a function that gets stock abbreviations given a stock name.
def getStockAbbrev(name) :
  return StD.get(name)
#End of the function getStockAbbrev.py
##################################################################################

##################################################################################

#A program for plotting the daily stock price.
def visualizeDailyStockPrice(data, stockAbbrev, dateTime, plotFilePath) :
  """

   NAME: visualizeDailyStockPrice(data, stockAbbrev, dateTime)
           
   PURPOSE: Plot the stock price for a given day as a function of time.
             
   CATEGORY:  Data Analysis
              
   CALLING SEQUENCE:  Called by GetStockData*.py
  
   INPUTS:  
           data : The numpy data array containing the time and price of the stock
           stockAbbrev : A string containing the abbreviation of the company whose
                  stock price we are collecting.
           dateTime :  A string containing the yearmonthdayhourminute that the query
                  function was started.
           plotFilePath : The path to where the plots will be saved.
  
   OPTIONAL INPUTS: None
                  
   KEYWORD PARAMETERS: None
                  
   OUTPUTS: A true or false flag.  At this time I am doing nothing with it but I may
            change the flag depending on how well the function performed.  As of right
            now the function works exactly as expected.
                 
   OPTIONAL OUTPUTS: None
                   
   SIDE EFFECTS:  The data is plotted and saved to a file.
                   
   RESTRICTIONS: None
                   
   EXAMPLE: succeed = gsf.visualizeDailyStockPrice(data, stockAbbrev, dateTime)

   MODIFICATION HISTORY:
             Written by jdw on May 25, 2020

  """

  import matplotlib.pyplot as plt
  import numpy as np
  from matplotlib.backends.backend_pdf import PdfPages
  import math
  import filePaths as fp
  
  #Put the price and time into separate vectors.
  time = data[:, 0]
  price = data[:, 1]
  
  #Generate the name of the the company for which we are interested.
  stockName = getStockName(stockAbbrev)
  
  #Create a output file name to where the plot will be saved.

  outfilename = stockName + 'DailyStockPrice' + dateTime + '.pdf'
  outfile = plotFilePath + outfilename
      
  numHalfHours = 13
  dpperhalfhour = math.ceil(len(price)/numHalfHours)
  
  tickval = np.array(np.append(0.0,  [float(dpperhalfhour*(2*i - 1)) for i in range(1,8)]))

  #Create a time vector.
  t = np.arange(1, len(price) + 1)
  
  #Get the date for the data.
  monthNameStr = convertMonthNumToMonthName(int(month))
  dateStr = (monthNameStr + ' ' + day + ' ' + year)
    
  #Create a title string.
  titlestr = ('Stock Price vs Time for ' + dateStr + ' - ' + stockName)

  #Lets make sure we have a clean canvas.
  plt.close('all')

  plt.figure()
  plt.plot(t, price, 'b')
  plt.grid('on')
  plt.title(titlestr, fontsize = 9)
  plt.ylabel('Stock Price(Dollars)')
  plt.xlabel('Time')
  plt.xticks(tickval, ('7:30 ',
                       '8:00AM','9:00AM','10:00AM','11:00AM','12:00PM','1:00PM','2:00PM'),
             fontsize = 7)
  
  #Save the plot to a file.
  pp = PdfPages(outfile)
  pp.savefig()
  pp.close()

  plt.cla()
  plt.clf()
  #End of the for loop - for filename in infiles :

  return True
#End of the function visualizeDailyStockPrice.py
####################################################################################

####################################################################################

def query(numSec, sleepTime, stockAbbrev, dateTime, dataFilePath) :
  """

   NAME:  query(numSec, sleepTime, stockAbbrev, dateTime) :
           
   PURPOSE:  A function that requests sale price information from the IEX stock server.
             
   CATEGORY:  Data Collection
              
   CALLING SEQUENCE:  Called by the various GetStockData*.py
  
   INPUTS:
            numSec : An integer variable that limits the number of seconds the query function
                     will operate. Without this variable the function will run for ever.
            sleepTime : An integer variable holding the length of time the function should 
                     sleep between querying the IEX server.  If this is to small(i.e. 1 second) 
                     the server will back up and the data will not be collected at even intervals.
            stockAbbrev : A string containing the company name as an abbreviation.
            dateTime : A string containing the yearmonthdayhourminute that the query
                     function was started.
            dataFilePath : The path to where the data file will be saved.
  
   OPTIONAL INPUTS: None
                  
   KEYWORD PARAMETERS: None
                  
   OUTPUTS: A numpy array containing the times(in milliseconds since 1970) the prices 
            were collected and the corresponding stock price.
                 
   OPTIONAL OUTPUTS: None
                   
   SIDE EFFECTS: None
                   
   RESTRICTIONS: None
                   
   EXAMPLE:  data = gsf.query(numSec, sleepTime, stockAbbrev, dateTime)
  
   MODIFICATION HISTORY:
             Written by jdw on May 25, 2020

  """

  import json, urllib.request
  import numpy as np
  import time
  sys.path.append('/home/jdw/UM2020Spring/M567/Functions/')
  import StockFunctions as sf

  
  #Value used by IEX to output the data.
  token ='pk_871cfbde34a04823ba26850dfb9134b8'

  #Create a value for a counter.
  n = 0

  #Create two lists.  LSP is for the last sale price and LST is for the last sale time.
  LSP = []
  LST = []

  #Generate a file name for the file to be written.
  stockDir = getStockName(stockAbbrev)
  fname = 'StockPrice_' + str(stockAbbrev) + dateTime + '.txt'
  filename = dataFilePath + fname

  #Run a while loop until the data is collected.
  while True:
      try:
          #Access the IEX api to get the data.
          html = urllib.request.urlopen("https://cloud.iexapis.com/stable/tops?token=" + token +
                                      "&symbols=" + tag)

          #The data are returned as a list of dictionaries.
          #Each dictionary corresponding to a different stock.
          lst = json.loads(html.read().decode('utf-8'))

          #We are only looking at one stock so lets get rid of the list and create a dictionary.
          d = lst[0]
        
          #We are interested in the last sale price in the dictionary.
          LSP.append(d.get("lastSalePrice"))
        
          #We are interested in the last sale time in the dictionary.
          #This time is given in milliseconds since January 1, 1970.
          #Leap seconds are not included.  This means that there will be approximately
          #a 30 second difference in the time given and the time decoded by the time
          #functions available to python, since there have been about 30 leap seconds
          #since 1970.
          LST.append(d.get("lastSaleTime"))
        
          #Increment the counter.
          n += 1
        
          #Every hour we will write or append the data to a file.
          if(time.localtime()[4] == 59) :
              val = writeFile(LST, LSP, filename)
              LSP = []
              LST = []
          #End of the if statement - if(time.localtime()[4] == 59):  
          #Lets get out of the loop if we have collected the number of samples we want.
          if (n == numSec) :
              break
          #End of the if statement - if(n == numSec) :
          
          #Lets get out of the loop if we are still running after 2:00 PM.
          if (time.localtime()[3] >= 14) :
              break
          #End of the if statement - if (time.localtime()[3] >= 14) :
          
          #Let us get a SleepTime length of  data.
          time.sleep(sleepTime)
        
      except:
        print('No return on iteration{0:d} for stock : {1} '.format(n, tag))
      #End of the try/except structure 
  #End of the while loop

  #Now create numpy arrays out of the lists.
  out_tuple = (LST, LSP) 
  out_arr = np.asarray(out_tuple)  
  return out_arr
              
#End of the function query.py
#################################################################################

#################################################################################

def getArgs(parser) :
 
  #Get the stock abbreviation parameter.
  parser.add_argument('-sa', '--StockAbbrev', default = 'amzn',
                      help = 'Choose how many iterations are made before stopping.', type = str)

  #Get the plot file path parameter.
  parser.add_argument('-pfp', '--plotFilePath', default = '/home/jdw/UM2020Spring/M567/Data/',
                      help = 'Choose the path to which the plots will be written.', type = str)

  #Get the data file path parameter.
  parser.add_argument('-dfp', '--dataFilePath', default = '/home/jdw/UM2020Spring/M567/Data/',
                      help = 'Choose the root path to which the data will be saved.', type = str)

  #Get the sleep time parameter.
  parser.add_argument('-st', '--sleepTime', default = 10.0,
                      help = 'Choose the sleep time between data queries.', type = float)

  
  args = parser.parse_args()

  #Generate variables from the inputs.
  stockAbbrev = args.stockAbbrev
  plotPath = args.plotFilePath
  dataPath = args.dataFilePath
  sleepTime = args.sleepTime
  
  #Convert the stock abbreviation into a full stock name.
  stockName = getStockName(stockAbbrev)

  #Write out the file paths.
  plotFilePath = plotPath + str(stockName) + '/'
  dataFilePath = dataPath + str(stockName) + '/'
  
  return stockAbbrev, plotFilePath, dataFilePath, sleepTime
#End of the function getArgs(parser).py

#################################################################################

#################################################################################

#Gather our code in a main() function.
def main() :
    import sys
    import time
    import argparse
    
    #First we get some data.  This function returns an array of times and prices.
    #First set the length of time to get.
    numHours = 6
    numSec = numHours * 360

    #Let us get the date and time.
    dt = time.localtime()
    yearStr = str('{0:02d}'.format(dt.tm_year))
    monthStr = str('{0:02d}'.format(dt.tm_mon))
    dayStr = str('{0:02d}'.format(dt.tm_mday))
    hourStr = str('{0:02d}'.format(dt.tm_hour))
    minuteStr = str('{0:02d}'.format(dt.tm_min))

    dateTime = (yearStr + monthStr + dayStr + hourStr + minuteStr)

    #Set up the argument parser.
    parser = argparse.ArgumentParser()

    #The name of the stock we are looking at.
    stockAbbrev, plotFilePath, dataFilePath, sleepTime = getArgs(parser)

    #Now get the data from the IEX server.
    data = query(numSec, sleepTime, stockAbbrev, dateTime, dataFilePath)

    #Now plot the data.
    succeed = visualizeDailyStockPrice(data, stockAbbrev, dateTime, plotFilePath)
    
# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
