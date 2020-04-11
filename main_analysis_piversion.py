################################################################
# READING & TRANSPOSING 

################################################################
from bs4 import BeautifulSoup as bs 
import time, os
import pandas as pd
from txtanalysis import DataCleaner as DC
import datetime

now = datetime.datetime.now()
print(now)
datum = now.strftime('%d-%m-%Y-')
date = '01-04-2020'

num = 1

def reading_file():
	""" ÖFFNEN DER FILES MIT PANDAS UND DANN IN EINE LISTE CONVERTEN  """
	os.chdir('/media/pi/datadrive/databank/welt_output')
	v_num_ls = ['13','9']
	article_list = list()
	for v_num in v_num_ls:
		var_datum = '01-04-2020-'
		version = var_datum + v_num +'-welt_data' + '.csv'
		print("Artikel_Version== ", version) 
		colnames =['headline','time','summary','article']
		df = pd.read_csv(f'{version}', header= None)
		article = df.iloc[[3]]
		article_list.append(article)
	art1 = article_list[0].values.tolist()
	art1 = art1[0]
	art2 = article_list[1].values.tolist()
	art2 = art2[0]
	return art1, art2

def reshape(art1, art2):
	print(type(art1))
	aa = [i.split(".") for i in art1]
	aa = aa[0]
	bb = [i.split(".") for i in art2]
	bb = bb[0]
	löschen = ['  Die WELT als ePaper: Die vollständige Ausgabe steht Ihnen bereits am Vorabend zur Verfügung – so sind Sie immer hochaktuell informiert', ' Weitere Informationen: http://epaper', 'welt', 'de  Der Kurz-Link dieses Artikels lautet: https://www', 'welt', 'de/206947223 ', '   Die WELT als ePaper: Die vollständige Ausgabe steht Ihnen bereits am Vorabend zur Verfügung – so sind Sie immer hochaktuell informiert','de']
	art1 = []
	for i in aa: 
		if i in löschen:
			continue
		art1.append(i)
	art2 = [i for i in bb if i not in löschen]
	# print(art1)
	c_art1 = DC.clean_list(art1)
	c_art2 = DC.clean_list(art2)
	return c_art1, c_art2

def open_nrc(path):
	# nrc = pd.read_csv()

	# nrc_file = open('PATH', encoding="utf8")
	# nrc_data_list = [i for i in nrc_file]

	pass
	
def compare_text_with_nrc(file1, file2):
	pass

def create_result_output():
	pass

# EXECUTE 
# INPUT : VERSIONSNAME bei reading file
art1, art2 = reading_file()
c_art1, c_art2 = reshape(art1, art2)



def output_processing1(file):
	pass




















