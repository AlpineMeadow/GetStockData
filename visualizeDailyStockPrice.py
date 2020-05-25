#! /usr/bin/env python3



##################################################################################
#Define a dictionary of the stock abbreviations and names.
def GetStockNames(abbrev) :
  import StockDict as sd
  return list(sd.StD.keys())[list(sd.StD.values()).index(abbrev)]
#End of the function GetStockNames.py
##################################################################################


