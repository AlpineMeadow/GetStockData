#! /usr/bin/env python3

#A program to get stock data.

def writeFile(LST, LSP, tag) :
#    breakpoint()
    import csv, time
    import numpy as np
    import os.path
    from os import path
    import sys
    sys.path.append('/home/jdw/UM2020Spring/M567/Functions/')
    import StockFunctions as sf
    
    timeNonzero = np.nonzero(LST)
    t_vals = time.localtime(LST[timeNonzero[0][0]]/1000.0)

    #Convert the integers to strings and prepend 0's to those values which
    #are less than 10.
    year = str('{0:04d}'.format(t_vals[0]))
    month = str('{0:02d}'.format(t_vals[1]))
    day = str('{0:02d}'.format(t_vals[2]))
    hour = str('{0:02d}'.format(t_vals[3]))
    minute = str('{0:02d}'.format(t_vals[4]))

    #Create a string for the date and time that the data were collected.    
    dateTime = year+month+day+hour+minute

    stockDir = sf.GetStockNames(tag)
    dirpath = '/home/jdw/UM2020Spring/M567/Data/' + stockDir + '/'
    fname = 'StockPrice_' + str(tag) + dateTime + '.txt'
    filename = dirpath + fname

    #Write the data to a file.
    if(path.exists(filename)) :
        #Append to the file.
        with open(filename, mode='a') as f :
            stock_writer = csv.writer(f, delimiter=',')
            for i in range(len(LST)) :
                stock_writer.writerow([LST[i], LSP[i]])            

    else :
        #Write the file.
        with open(filename, mode='w') as f :
            stock_writer = csv.writer(f, delimiter=',')
            for i in range(len(LST)) :
                stock_writer.writerow([LST[i], LSP[i]])            

    return True

#A function that requests sale price information from the IEX stock exchange.
def query(numSec, sleepTime, tag) :
    import json, urllib.request
    import numpy as np
    import time
    
    #Value used by IEX to output the data.
    token ='pk_871cfbde34a04823ba26850dfb9134b8'

    #Create a value for a counter.
    n = 0

    LSP = []
    LST = []
    
    #Run a while loop until the data is collected.
    while True:        
        try:
            #Access the IEX api to get the data.
            html = urllib.request.urlopen("https://cloud.iexapis.com/stable/tops?token=" + token +
                                          "&symbols="+tag)

            #The data are returned as a list of dictionaries.  Each dictionary corresponding to a different stock.
            lst = json.loads(html.read().decode('utf-8'))

            #We are only looking at one stock so lets get rid of the list and create a dictionary.
            d = lst[0]

            #We are interested in the last sale price in the dictionary.
            LSP.append(d.get("lastSalePrice"))
        
            #We are interested in the last sale time in the dictionary.  This time is given in milliseconds since
            #January 1, 1970.  Leap seconds are not included.  This means that there will be approximately
            #a 30 second difference in the time given and the time decoded by the time functions available to
            #python, since there have been about 30 leap seconds since 1970.
            LST.append(d.get("lastSaleTime"))

            #Increment the counter.
            n += 1

            #Every hour we will write or append the data to a file.
            if(time.localtime()[4] == 59) :
                val = writeFile(LST, LSP, tag)
                
            #Lets get out of the loop if we have collected the number of samples we want.
            if (n == numSec) :
                break

            #Lets get out of the loop if we are still running after 2:00 PM.
            if (time.localtime()[3] >= 14) :
                break

            #Let us get a SleepTime length of  data.
            time.sleep(sleepTime)
        
        except:
            print('No return on iteration ',n)

    out_tuple = (LST, LSP) 
    out_arr = np.asarray(out_tuple)  
    return out_arr
#End of the function query.py


###############################################################################

###############################################################################

#Gather our code in a main() function.
def main() :

    #First we get some data.  This function returns an array of times and prices.
    #First set the length of time to get.
    numHours = 6
    numSec = numHours * 360
    sleepTime = 10

    #The name of the stock we are looking at.
    tag = 'goog'  #Google
    data = query(numSec, sleepTime, tag)
    
# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
