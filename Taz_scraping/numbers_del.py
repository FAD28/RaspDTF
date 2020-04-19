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
cc = 1 
os.chdir("/media/pi/datadrive/databank/TAZ-SCRAPING/processed_out/test")
for i in dp:
	df = pd.read_csv(i, delimiter=";")
	print("Pfad Nummer: ", cc, " / ", len(df))
	headline = list(df['headline'])
	print(headline)
	sleep(3)
	versionsname = DC.clean_filename([headline])

	df.to_csv(f"{versionsname}-{cc}.csv")
	cc += 1
