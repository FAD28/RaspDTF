import pandas as pd
import time, os
from txtanalysis import DataCleaner as DC
from txtanalysis import DataWrangling as DW

# tt = "/Volumes/datadrive/databank/WELT-SCRAPING/output/archiv/03-05-2020-1-welt_data.csv"
paths = DW.get_all_paths('/Volumes/datadrive/databank/WELT-SCRAPING/output')


cc = 1
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
	temp = open("6temp.csv",'w+')
	temp.write(data)
	temp.close()

	df2 = pd.read_csv("6temp.csv", sep=";", header= None)
	data2 = str(list(df2[2]))
	temp2 = open("6temp2.csv",'w+')
	temp2.write(data2)
	temp2.close()

	df3 = pd.read_csv("6temp2.csv", sep=";", header= None)
	data3 = str(list(df3[2]))
	temp3 = open("6temp3.csv",'w+')
	temp3.write(data3)
	temp3.close()

	df4 = pd.read_csv("6temp3.csv", sep=";", header= None)
	data4 = str(list(df4[2]))
	temp4 = open("6temp4.csv",'w+')
	temp4.write(data4+";"+filename)
	temp4.close()

	df5 = pd.read_csv("6temp4.csv", sep=";", header= None)
	data5 = str(list(df5[2]))
	temp5 = open("6temp5.csv",'w+')
	temp5.write(data5+","+filename)
	temp5.close()

	dfx = pd.read_csv("6temp5.csv", sep=",", header= None)
	########## PATH ##########
	os.chdir("/Volumes/datadrive/databank/WELT-SCRAPING/processing_out/last_processing")
	########## PATH ##########
	final_df = pd.DataFrame({'index': dfx[0], 'headline': dfx[1], 'time': dfx[2], 'summary':dfx[3], 'article': dfx[4], 'filename': dfx[5]})

	list_headline = list(final_df['headline'])
	try:
		file_article_name = DC.clean_filename(list_headline)
		f1 = open("/Volumes/datadrive/databank/WELT-SCRAPING/temp/2temp/Success_last_processing6.csv", 'a')
		f1.write(filename+"\n")
		f1.close()
	except:
		f2 = open("/Volumes/datadrive/databank/WELT-SCRAPING/temp/2temp/Errors_last_processing6.csv", 'a')
		f2.write(filename+"\n")
		f2.close()
		print("ERROR ^^^^^^^^^^^^^^^ ", filename)
		continue


	# Output
	file_new_name= f"{file_article_name}-{cc}.csv"
	print(final_df)
	final_df.to_csv(file_new_name, sep=";")
	print(file_new_name, " created successfully :) * * * * * * ")
	cc += 1
















