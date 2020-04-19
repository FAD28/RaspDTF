import spacy
from spacy_sentiws import spaCySentiWS
from time import sleep
import csv
import pandas as pd 
import datetime
from tqdm import tqdm
import itertools, re
import os
from txtanalysis import DataCleaner as DC 
from txtanalysis import DataWrangling as DW 
from txtanalysis.emotion import Emotionen_nrc as nrc 
from HanTa import HanoverTagger as ht

os.chdir("/media/pi/datadrive/databank/TAZ-SCRAPING/processed_out")

dp = list(set(DW.get_all_paths(os.getcwd())))
print(dp)
#sleep(10)
cc = 1 
os.chdir("/media/pi/datadrive/databank/TAZ-SCRAPING/processed_out/test")
for i in dp:
	try:
		df = pd.read_csv(i, delimiter=";")
		print("Pfad Nummer: ", cc, " / ", len(dp))
		print(i)
		headline = list(df['headline'])
		print(headline)
		versionsname = DC.clean_filename([headline][0])
		print(cc)
		df.to_csv(f"{versionsname}.csv")
		cc += 1
	except Exception as e:
		print("ERROR: ",e)

print("SUCCESS ---> CODE 0! :)")
	




