


#################################################################################
#Create a month name to be returned as  a string.
def convertMonthNumToMonthName(monthNum) :
  #This functions converts a month number of type integer to a month name of type string.
  if(monthNum == 1) :
    return 'Jan'
  elif(monthNum == 2) :
    return 'Feb'
  elif(monthNum == 3) :
    return 'Mar'
  elif(monthNum == 4) :
    return 'Apr'
  elif(monthNum == 5) :
    return 'May'
  elif(monthNum == 6) :
    return 'Jun'
  elif(monthNum == 7) :
    return 'Jul'
  elif(monthNum == 8) :
    return 'Aug'
  elif(monthNum == 9) :
    return 'Sep'
  elif(monthNum == 10) :
    return 'Oct'
  elif(monthNum == 11) :
    return 'Nov'
  elif(monthNum == 12) :
    return 'Dec'
  else :
    print('Error in calling convertMonthNumToMonthName.py')

#End of the function convertMonthNumToMonthName.py

#################################################################################

##################################################################################

#Define a function that gets stock abbreviations.
def GetStockAbbrev(name) :
    import sys
    sys.path.append('/home/jdw/UM2020Spring/M567/Scripts/')
    import StockDict as sd
    
    return sd.StD.get(name)
#End of the function GetStockAbbrev.py
##################################################################################

##################################################################################

#Define a dictionary of the stock abbreviations and names.
def getStockName(abbrev) :
    import sys
    sys.path.append('/home/jdw/UM2020Spring/M567/Scripts/')
    import StockDict as sd
    
    return list(sd.StD.keys())[list(sd.StD.values()).index(abbrev)]
#End of the function getStockNames.py
##################################################################################



#################################################################################
def writeFile(LST, LSP, filename) :
  """

   NAME:  writeFile(LST, LSP, filename) :
           
   PURPOSE:  Write a date file of the last sale time(LST) and last sale price(LSP)
             
   CATEGORY:  Data Collection
              
   CALLING SEQUENCE:  Called by query.py
  
   INPUTS:
             LST : A list of times.  This is expected to be the times in a given hour of data
                   collection.
             LSP : A list of stock prices.  This is expected to be the prices in a given
                   hour of data collection.
             filename : The name of the file into which the data will be read.
  
   OPTIONAL INPUTS:  None
                  
   KEYWORD PARAMETERS: None
                  
   OUTPUTS: A true or false flag.  At this time I am doing nothing with it but I may
            change the flag depending on how well the function performed.  As of right
            now the function works exactly as expected.  
                 
   OPTIONAL OUTPUTS:  None
                   
   SIDE EFFECTS:  The data are written to a file of name filename.
                   
   RESTRICTIONS: None
                   
   EXAMPLE: val = writeFile(LST, LSP, filename)
  
   MODIFICATION HISTORY:
             Written by jdw on May 25, 2020

  """

  import csv, time
  import numpy as np
  import os.path
  from os import path
    
  #Write the data to a file.
  if(path.exists(filename)) :
      #Append to the file.
      with open(filename, mode = 'a') as f :
          stock_writer = csv.writer(f, delimiter=',')
          for i in range(len(LST)) :
              stock_writer.writerow([LST[i], LSP[i]])
          #End of the for loop - for i in range(len(LST)):
      #End of the with statement - with open(filename, mode='a') as f :

  else :
      #Write the file.
      with open(filename, mode = 'w') as f :
          stock_writer = csv.writer(f, delimiter=',')
          for i in range(len(LST)) :
              stock_writer.writerow([LST[i], LSP[i]])
          #End of the for loop - for i in range(len(LST)):
      #End of the with statement - with open(filename, mode='w') as f :

  return True
#End of the functions writeFile.py
#################################################################################

#################################################################################
def query(numSec, sleepTime, stockAbbrev, dateTime) :
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
  
   OPTIONAL INPUTS: None
                  
   KEYWORD PARAMETERS: None
                  
   OUTPUTS: A numpy array containing the times the prices were collected and the
            corresponding stock price.
                 
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
  stockDir = getStockNames(stockAbbrev)
  dirpath = '/home/jdw/UM2020Spring/M567/Data/' + stockDir + '/'
  fname = 'StockPrice_' + str(stockAbbrev) + dateTime + '.txt'
  filename = dirpath + fname

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

##################################################################################
#A program for plotting the daily stock price.

#Gather our code in a main() function.
def visualizeDailyStockPrice(data, stockAbbrev, dateTime) :
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

  #Put the price and time into separate vectors.
  time = data[:,0]
  price = data[:,1]
  
  #Generate the name of the the company for which we are interested.
  stockName = getStockName(stockAbbrev)
  
  #Create a output file name to where the plot will be saved.
  outfilepath = '/home/jdw/UM2020Spring/M567/Data/' + stockName + '/'
  outfilename = stockName + 'DailyStockPrice' + dateTime + '.pdf'
  outfile = outfilepath + outfilename
      
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


