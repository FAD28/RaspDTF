import spacy
from spacy_sentiws import spaCySentiWS
import time 
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
from collections import Counter
import statistics

os.chdir("/Volumes/datadrive/databank/TAZ-SCRAPING/final_data")

dp = DW.get_all_paths(os.getcwd())

print("DIE ANZAHL DER PFADE: ", len(dp))
nlp = spacy.load('de')
sentiws = spaCySentiWS(sentiws_path='/Volumes/datadrive/databank/TAZ-SCRAPING/RaspDTF/SentiWS_v2.0')
nlp.add_pipe(sentiws)

counter = 1
for version in dp:
    print(f"{version} -------> {counter}/{len(dp)}")
    df = pd.read_csv(version, sep=";")
    print(list(df['article']))
    print("_____________________________")
    time.sleep(4)
