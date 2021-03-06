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

os.chdir('/Users/Fabi/PycharmProjects/Thesis/ANALYSIS/Thesis')

daten_pfade = DW.get_all_paths(os.getcwd())
nlp = spacy.load('de')
sentiws = spaCySentiWS(sentiws_path='/Users/Fabi/PycharmProjects/Spacy/SentiWS_v2.0')
nlp.add_pipe(sentiws)
print("\n".join(daten_pfade))
#print(len(daten_pfade))

testpfad = "/Users/Fabi/PycharmProjects/Thesis/ANALYSIS/Thesis/Sued_sample/1-Gesundheit--Düsseldorf--Geplantes-EpidemieGesetz-kommt-auf-den-Prüfstand.csv"

final_df = pd.DataFrame()
sleep(500)
for pfad in daten_pfade[:18]:
	df = pd.read_csv(pfad, sep = ";")
	x = [i.split() for i in list(df['article'])][0]
	print("ANZAHl an Wörtern im Artikel:", len(x))
	# sleep(3)
	head = [i for i in df['headline']]
	print(str(head))
	print("::::: SENTIWS ::::")
	tagger = ht.HanoverTagger("morphmodel_ger.pgz")
	lx = [tagger.analyze(i)[0] for i in x]
	polarity_scores = []
	found_words = []
	for i in lx: 
		doc = nlp(i)
		for t in doc: 
			if t._.sentiws != None:
				tupi = (t.text,t._.sentiws)
				polarity_scores.append(tupi)
				found_words.append(t.text)
	total_polarity = round(sum(n for _, n in polarity_scores)/len(found_words),4)

	# sleep(3)
	print("::::: NRC ::::")
	lxlw = [i.lower() for i in lx]
	zorn, erwart, ekel, furcht, freude, trauer, überr, vertrauen = nrc.NRC_analysis(lxlw)
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
	'total_polarity': [total_polarity],
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
	'polarity_scores': [polarity_scores]
	}
	newdf = pd.DataFrame(complete_data, columns = complete_data.keys())
	pd.set_option('display.max_rows', 500)
	pd.set_option('display.max_columns', 500)
	pd.set_option('display.width', 1000)
	# sleep(2)
	final_df = pd.concat([final_df, newdf], axis = 0, ignore_index= True).reset_index(drop=True)
	#print(final_df)
final_df.to_csv('Sued_results.csv', sep=";")
print(" ----------------> SUCCESS= File: Sued_results.csv created * * * <----> CODE 0")








