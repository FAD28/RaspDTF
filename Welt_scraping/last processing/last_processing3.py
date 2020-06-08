import pandas as pd
import time, os
from txtanalysis import DataCleaner as DC
from txtanalysis import DataWrangling as DW

testfile= "/Volumes/datadrive/databank/WELT-SCRAPING/output/archiv/01-04-2020-1-welt_data.csv"
# filename = os.path.basename(testfile)
paths = DW.get_all_paths('/Volumes/datadrive/databank/WELT-SCRAPING/output')

cc = 1
for version in paths: 
	filename = os.path.basename(version)

	print("________________")
	print("Filename = ", filename)
	print(version)
	print("________________")
	
	df = pd.read_csv(version, sep=";")
	data = str(list(df['time']))

	########## PATH ##########
	os.chdir("/Volumes/datadrive/databank/WELT-SCRAPING/temp/2temp")
	########## PATH ##########

	temp = open("2temp.csv",'w+')
	temp.write(data)
	temp.close()

	df2 = pd.read_csv("2temp.csv", sep=";", header= None)
	data2 = str(list(df2[2]))
	temp2 = open("2temp2.csv",'w+')
	temp2.write(data2+";"+filename)
	temp2.close()

	df3 = pd.read_csv("2temp2.csv", sep=";", header= None)
	final_df = pd.DataFrame({'index': df3[0], 'headline': df3[1], 'time': df3[2], 'summary':df3[3], 'article': df3[4], 'filename':df3[5]})
	
	########## PATH ##########
	os.chdir("/Volumes/datadrive/databank/WELT-SCRAPING/processing_out/last_processing")
	########## PATH ##########
	list_headline = list(final_df['headline'])
	file_article_name = DC.clean_filename(list_headline)

	# Output
	file_new_name= f"{file_article_name}-{cc}.csv"
	final_df.to_csv(file_new_name, sep=";")
	print(file_new_name, " created successfully :) * * * * * * ")
	cc += 1

