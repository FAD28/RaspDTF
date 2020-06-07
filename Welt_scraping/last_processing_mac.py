####################################################################################
# NEW CODE
##

import pandas as pd 
from txtanalysis import DataCleaner as DC
from txtanalysis import DataWrangling as DW
import time, os
import glob

paths = DW.get_all_paths('/Volumes/datadrive/databank/WELT-SCRAPING/output')

def last_processing():
	cc = 1
	for version in paths:
		
		# Path oder Version
		filename = os.path.basename(version)

		print("________________")
		print("Filename = ", filename)
		print("________________")

		# Filtern aus Column Time
		df = pd.read_csv(p, sep=";")
		half_data = str(list(df['time']))
		data = half_data+";"+filename

		########## PATH ##########
		os.chdir("/Volumes/datadrive/databank/WELT-SCRAPING/temp")
		########## PATH ##########

		f = open('temp.csv','w+')
		f.write(data)

		# Neu einlesen und second Filtern
		df1 = pd.read_csv('temp.csv', sep=";",header= None)
		half_data2 = str(list(df1[2]))
		data1 = half_data2+";"+filename
		f1 = open('temp2.csv','w+')
		f1.write(data1)

		# Neu einlesen und dann neues Frame basteln
		df2 = pd.read_csv('temp2.csv', sep=";", header= None)
		final_df = pd.DataFrame({'index': df2[0], 'headline': df2[1], 'time': df2[2], 'summary':df2[3], 'article': df2[4], 'filename':df2[5]})

		# Headline
		list_headline = list(final_df['headline'])
		file_article_name = DC.clean_filename(list_headline)
		
		########## PATH ##########
		os.chdir("/Volumes/datadrive/databank/WELT-SCRAPING/processing_out/last_processing")
		########## PATH ##########

		# Output
		file_new_name= f"{file_article_name}-{cc}.csv"
		final_df.to_csv(file_new_name, sep=";")
		print(file_new_name, " created successfully :) * * * * * * ")
		cc += 1















