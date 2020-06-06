# Welt Processing 

import pandas as pd 
from txtanalysis import DataCleaner as DC
from txtanalysis import DataWrangling as DW
import time, os
import glob

os.chdir("/media/pi/datadrive/databank/WELT-SCRAPING/output")
paths = DW.get_all_paths('/media/pi/datadrive/databank/WELT-SCRAPING/output')

for version in paths:
	print(version)
	df = pd.read_csv(version, sep = ';', header=0)
	time.sleep(1)
	print(df)
	print("________________")
	data = list(df['time'])
	print("***	Daten: 		", data)
	print("_______________________________")
	df['filename']= os.path.basename(version)	
	print(df)
	time.sleep(1)
















