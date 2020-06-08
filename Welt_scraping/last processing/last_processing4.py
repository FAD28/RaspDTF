import pandas as pd
import time, os
from txtanalysis import DataCleaner as DC
from txtanalysis import DataWrangling as DW

#testfile= "/Volumes/datadrive/databank/WELT-SCRAPING/output/archiv/25-03-2020-1-welt_data.csv"
#filename = os.path.basename(testfile)
paths = DW.get_all_paths('/Volumes/datadrive/databank/WELT-SCRAPING/output')

cc=1
for version in paths:
	filename = os.path.basename(version)
	print("________________")
	print("Filename = ", filename)
	print(version)
	print("________________")

	########## PATH ##########
	os.chdir("/Volumes/datadrive/databank/WELT-SCRAPING/temp/2temp")
	########## PATH ##########
	df = pd.read_csv(version, sep=";")
	data = str(list(df['time']))
	temp = open("3temp.csv",'w+')
	temp.write(data)
	temp.close()

	df2 = pd.read_csv("3temp.csv", sep=";", header= None)
	data2 = str(list(df2[2]))
	temp2 = open("3temp2.csv",'w+')
	temp2.write(data2)
	temp2.close()

	df3 = pd.read_csv("3temp2.csv", sep=";", header= None)
	final_df = pd.DataFrame({'index': df3[0], 'headline': df3[1], 'time': df3[2], 'summary':df3[3], 'article': df3[4]})
	final_df.to_csv("3temp3.csv", sep=";")

	dff = pd.read_csv("3temp3.csv", sep=";")
	data3 = str(list(dff['time']))
	temp3 = open("3temp4.csv", 'w+')
	temp3.write(data3+";"+filename)
	temp3.close()

	df4 = pd.read_csv("3temp4.csv", sep=";", header=None)
	########## PATH ##########
	os.chdir("/Volumes/datadrive/databank/WELT-SCRAPING/processing_out/last_processing")
	########## PATH ##########
	final_df2 = pd.DataFrame({'index': df4[0], 'headline': df4[1], 'time': df4[2], 'summary':df4[3], 'article': df4[4], 'filename': df4[5]})
	
	list_headline = list(final_df2['headline'])
	try:
		file_article_name = DC.clean_filename(list_headline)
		f1 = open("/Volumes/datadrive/databank/WELT-SCRAPING/temp/2temp/Success_last_processing4.csv", 'a')
		f1.write(filename+"\n")
		f1.close()
	except:
		f2 = open("/Volumes/datadrive/databank/WELT-SCRAPING/temp/2temp/Errors_last_processing4.csv", 'a')
		f2.write(filename+"\n")
		f2.close()
		print("ERROR ^^^^^^^^^^^^^^^ ", filename)
		continue
	# Output
	file_new_name= f"{file_article_name}-{cc}.csv"
	final_df2.to_csv(file_new_name, sep=";")
	print(file_new_name, " created successfully :) * * * * * * ")
	cc += 1

