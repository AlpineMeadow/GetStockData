
#A function that will write the data.
def WriteStockData(LST, LSP, tag) :
    import time
    import os.path
    from os import path
    
    #There are times when the data are returned as 0,0 instead of time,price.  So search for the
    #first valid time stamp
    timeNonzero = LST[LST > 0.0]
    t_vals = time.localtime(timeNonzero[0]/1000.0)

    #Convert the integers to strings and prepend 0's to those values which
    #are less than 10.
    year = str('{0:02d}'.format(t_vals[0]))
    month = str('{0:02d}'.format(t_vals[1]))
    day = str('{0:02d}'.format(t_vals[2]))
    hour = str('{0:02d}'.format(t_vals[3]))
    minute = str('{0:02d}'.format(t_vals[4]))

    #Create a string for the date and time that the data were collected.    
    dateTime = year+month+day+hour+minute

    stockDir = GetStockNames(tag)
    path = '/home/jdw/UM2020Spring/M567/Data/' + stockDir + '/'
    fname = 'StockPrice_' + str(tag) + dateTime + '.txt'
    filename = path + fname

    if(path.exists(filename)) :    
        #Write the file with columns of time and price.
        with open(filename, mode='a') as f :
            file_writer = csv.writer(f, delimiter=',')
            for i in range(numSec) :
                file_writer.writerow([LST[i], LSP[i]])            
            #End of the for loop - for i in range(numSec):
    else : #File does not exist so write it.
        #Write the file with columns of time and price.
        with open(filename, mode='w') as f :
            file_writer = csv.writer(f, delimiter=',')
            for i in range(numSec) :
                file_writer.writerow([LST[i], LSP[i]])            
            #End of the for loop - for i in range(numSec):
    #End of if else clause.
    
#End of the function WriteStockData.py            

#A function that requests sale price information from the IEX stock exchange.
def query(numSec, sleepTime, tag) :
    import csv, json, urllib.request, time
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
            
            #Lets get out of the loop if we have collected the number of samples we want.
            if (n == numSec) :
                break
            
            #Write the data every hour.
            if(int(time.localtime()[4])%59 == 0) :
               WriteStockData(LST, LSP, tag)
            #End of if statement if(int(time.localtime()%4 == 0)
               
            #Lets get out of the loop if we are still running after 2:00 PM.
            if (int(time.localtime()[3]) >= 14) :
              break

            #Let us get a SleepTime length of  data.
            time.sleep(sleepTime)
        
        except:
            print('No return on iteration ',n)

    out_tuple = (LST, LSP) 
    out_arr = np.asarray(out_tuple)  
    return out_arr
#End of the function query.py
