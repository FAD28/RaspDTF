# Welt Processing 

import pandas as pd 
from txtanalysis import DataCleaner as DC
from txtanalysis import DataWrangling as DW
import time

paths = DW.get_all_paths('/media/pi/datadrive/databank/WELT-SCRAPING/output')

for version in path:
	df = pd.read_csv(version, sep = ';', header=0)
	time.sleep(10)
	print(df)
