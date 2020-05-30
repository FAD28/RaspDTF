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
from collections import Counter
import statistics


os.chdir("/media/pi/datadrive/databank/TAZ-SCRAPING/processed_out/unique_files")

dp = list(set(DW.get_all_paths(os.getcwd())))
daten_pfade = list(set(dp)) 
print("DIE ANZAHL DER LINKS IST: ", len(daten_pfade))
nlp = spacy.load('de')
sentiws = spaCySentiWS(sentiws_path='/media/pi/datadrive/databank/TAZ-SCRAPING/RaspDTF/SentiWS_v2.0')
nlp.add_pipe(sentiws)
#print("\n".join(daten_pfade))
#print(len(daten_pfade))

#testpfad = "/Users/Fabi/PycharmProjects/Thesis/ANALYSIS/Thesis/Sued_sample/1-Gesundheit--Düsseldorf--Geplantes-EpidemieGesetz-kommt-auf-den-Prüfstand.csv"
cxl = 1
final_df = pd.DataFrame()
total_paths = len(daten_pfade)
for pfad in daten_pfade:
	try:
		print(f"LINK:{pfad}	*--------*   {cxl} / {total_paths}   ")
		df = pd.read_csv(pfad, sep = ";")
		print(df)
		x = [i.split() for i in list(df['article'])][0]
		xart = " ".join(x)
		print("ANZAHl an Wörtern im Artikel:", len(x))
		head = [i for i in df['headline']]
		print(str(head))
		print("::::: SENTIWS ::::")
		tagger = ht.HanoverTagger("morphmodel_ger.pgz")
		lx = [tagger.analyze(i)[0] for i in x]
		polarity_scores = []
		found_words = []
		just_polarity = []
		xx = 0
		for i in tqdm(lx): 
			doc = nlp(i)
			for t in doc: 
				if t._.sentiws != None:
					tupi = (t.text,t._.sentiws)
					polarity_scores.append(tupi)
					found_words.append(t.text)
					just_polarity.append(t._.sentiws)
					xx += 1
		mean = statistics.mean(just_polarity)
		median = statistics.median(just_polarity)
		stdev = statistics.stdev(just_polarity)
		variance = statistics.variance(just_polarity)
		total_polarity = round(sum(n for _, n in polarity_scores)/len(found_words),4)
		stp_wörter = DW.load_stopwords()
		x_ohne_stp = DW.remove_stopwords(x, stp_wörter)
		len_ohne_stp = len(x_ohne_stp)
		sentiment_index = xx / len(x_ohne_stp)
		print("Total Polarity = ", total_polarity)
		print("::::: NRC ::::")
		#lxlw = [i.lower() for i in lx]
		emotionsindex, my_faktor, zorn, erwart, ekel, furcht, freude, trauer, überr, vertrauen = nrc.NRC_analysis(lx) # ehemalig lxlw
		cwords = len(x)
		czorn = len(zorn)
		cewar = len(erwart)
		cekel = len(ekel)
		cfurc = len(furcht)
		cfreu = len(freude)
		ctrau = len(trauer)
		cüber = len(überr)
		cvert = len(vertrauen)
		complete_data = {
		'headline': head,
		'total_words': [cwords],
		'total_words_nostp': len_ohne_stp, 
		'total_polarity': [total_polarity],
		'mean_polarity': [mean],
		'median_polarity': [median],
		'stdev_polarity': [stdev],
		'variance_polarity': [variance],
		'emotions_index': [emotionsindex],
		'sentiment_index': [sentiment_index],
		'zorn_count': [czorn],
		'erwartung_count': [cewar],
		'ekel_count': [cekel],
		'furcht_count': [cfurc],
		'freude_count': [cfreu],
		'trauer_count': [ctrau],
		'überraschung_count': [cüber],
		'vertrauen_count': [cvert],
		'zorn_words': [zorn],
		'erwartung_words': [erwart],
		'ekel_words': [ekel],
		'furcht_words': [furcht],
		'freude_words': [freude],
		'trauer_words': [trauer],
		'überraschung_words': [überr],
		'vertrauen_words': [vertrauen],
		'polarity_scores': [polarity_scores],
		'article': [xart]
		}
		newdf = pd.DataFrame(complete_data, columns = complete_data.keys())
		pd.set_option('display.max_rows', 500)
		pd.set_option('display.max_columns', 500)
		pd.set_option('display.width', 1000)
		final_df = pd.concat([final_df, newdf], axis = 0, ignore_index= True).reset_index(drop=True)
		cxl += 1
	except Exception as e:
		print(e)
		continue
os.chdir("/media/pi/datadrive/databank/TAZ-SCRAPING/")
final_df.to_csv('TAZ_results.csv', sep=";")
print(" ----------------> SUCCESS= File: Sued_results.csv created * * * <----> CODE 0")








