#! /usr/bin/env python3


#A program for plotting the daily stock price.

#Gather our code in a main() function.
def main() :
  import matplotlib.pyplot as plt
  import numpy as np
  from matplotlib.backends.backend_pdf import PdfPages
  import math
  import argparse #A parser for command line options.
  import sys
  import csv
  import glob
  

  #Since python cannot figure out my path I append my function directory to the path.
  sys.path.append('/home/jdw/UM2020Spring/M567/Functions/')

  #Now import StockFunctions.py.
  import StockFunctions as sf

  #Create an argparse object.
#  parser = argparse.ArgumentParser()

  #Add some optional arguments.
  #Get the name of the company for which the stock prices were obtained.
#  stockNameHelp = 'Input the name of a company whose stock prices you want to visualize.'
#  parser.add_argument('-s','--stockName', help = stockNameHelp, default = 'Google')

  #Get the year the stock prices were obtained.
#  yearHelp = 'Input the year the stock price was obtained. Value is integer.'
#  parser.add_argument('-y', '--year', help = yearHelp, default = 2020, type = int)

  #Get the month the stock prices were obtained.
#  monthHelp = 'Input the month the stock price was obtained. Value is integer.'
#  parser.add_argument('-m', '--month', help = monthHelp, default = 3, type = int)

  #Get the day the stock prices were obtained.
#  dayHelp = 'Input the day the stock price was obtained.  Value is integer.'
#  parser.add_argument('-d', '--day', help = dayHelp, default = 2, type = int)

  #Get the input directory for the plot.
#  inputHelp = 'Input the full path of the directory in which the data is found.'
#  defaultInputDir = '/home/jdw/UM2020Spring/M567/Data/Google/'
#  parser.add_argument('-D','--Directory', help = inputHelp, default = defaultInputDir)

  #Get the output directory for the plot.
#  outputHelp = 'Input the full path of the directory in which to place the output file.'
#  defaultOutputDir = '/home/jdw/UM2020Spring/M567/Plots/'
#  parser.add_argument('-P','--Plots', help = outputHelp, default = defaultOutputDir)
  
  #Set the input arguments to the args object.
#  args = parser.parse_args()

  #Make up the input and output file names.
#  stockAbbrev = sf.GetStockAbbrev(args.stockName)
#  datetime = str(args.year) + str('{0:02d}'.format(args.month)) + str('{0:02d}'.format(args.day))

  #Choose a company whose stock price you want to visualize.
  stockName = 'Verizon'
  stockAbbrev = sf.GetStockAbbrev(stockName)

  directory = ('/home/jdw/UM2020Spring/M567/Data/' + stockName +
               '/StockPrice_' + stockAbbrev + '*.txt')
  
  infiles = glob.glob(directory)

  for filename in infiles :
    if(filename[-4:] == '.txt') :

      datetime = filename[-16 : -4]
      month = filename[-12 : -10]
      month = month.lstrip('0')
      day = filename[-10 : -8]
      day = day.lstrip('0')
      year = filename[-16 : -12]
      
      #Create a output file name to where the plot will be saved.
      outfilepath = '/home/jdw/UM2020Spring/M567/Data/' + stockName + '/'
      outfilename = stockName + 'DailyStockPrice' + datetime + '.pdf'
      outfile = outfilepath + outfilename

      
      #Open and read in the saved data.  We need to use infile[0] because glob returns a list.
      with open(filename) as csv_file :
        csv_reader = csv.reader(csv_file, delimiter = ',')
        line_count = 0
        dateTime = []
        price = []
        for row in csv_reader :
          dateTime.append(float(row[0]))
          price.append(float(row[1]))
        #End of the for loop - for row in csv_reader:
      #End of the with/open loop.

      numHalfHours = 13
      dpperhalfhour = math.ceil(len(price)/numHalfHours)
  
      tickval = np.zeros(8)
      for i in range(1, 8) :
        tickval[i] = dpperhalfhour*(2*i - 1)
      #End of the for loop - for i in range(1, 8) :

      #Create a time vector.
      t = np.arange(1, len(price) + 1)
  
      #Get the date for the data.
      monthNameStr = sf.convertMonthNumToMonthName(int(month))
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

# Standard boilerplate to call the main() function to begin
# the program.
if __name__ == '__main__':
  main()
