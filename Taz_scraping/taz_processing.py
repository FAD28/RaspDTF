import pandas as pd 
import os, time
from txtanalysis import DataCleaner as DC
from txtanalysis import DataWrangling as DW

os.chdir("/Users/Fabi/PycharmProjects/Thesis/ANALYSIS/Thesis/Taz_sample")
paths = DW.get_all_paths(os.getcwd())
print("\n".join(paths))

#tt = "/Users/Fabi/PycharmProjects/Thesis/ANALYSIS/Thesis/Taz_sample/05-04-2020-die_angst_geht_um.csv"

failed = []
cc = 1
for i in paths:
	datum = i[62:72]
	df = pd.read_csv(i, header = 0,delimiter= ";")
	colnames = list(df['0'])
	headline = df['1'][0]
	article = df['1'][1]
	meta_data = df['1'][2]
	intro_data = df['1'][3]
	h4_data = df['1'][4]
	comments_data = df['1'][5]
	author = df['1'][6]
	versionsname = DC.clean_filename([headline])
	new_dataformat= {
	'headline': [headline],
	'article': [article],
	'author': [author],
	'comments': [comments_data],
	'h4': [h4_data],
	'intro': [intro_data],
	'meta_data': [meta_data] }
	new_df = pd.DataFrame(new_dataformat)
	new_df.to_csv(f"{cc}-{versionsname}-{datum}.csv", sep= ";")
	cc += 1 
print("SUCCESS FILES HAVE BEEN CONVERTED * * *")
# 	#time.sleep(1)
# fail = open("failed.txt", "a")
# fail.write(str(failed))
