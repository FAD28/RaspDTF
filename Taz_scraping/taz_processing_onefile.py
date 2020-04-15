import pandas as pd 
import os, time
from txtanalysis import DataCleaner as DC
from txtanalysis import DataWrangling as DW

os.chdir("/Users/Fabi/PycharmProjects/Thesis/ANALYSIS/Thesis/Taz_sample")
paths = DW.get_all_paths(os.getcwd())
print("\n".join(paths))

#tt = "/Users/Fabi/PycharmProjects/Thesis/ANALYSIS/Thesis/Taz_sample/05-04-2020-die_angst_geht_um.csv"

final_df = pd.DataFrame()
failed = []
cc = 1
for i in paths:
	datum = i[62:72]
	df = pd.read_csv(i, header = 0,delimiter= ";")
	try:
		colnames = list(df['0'])
	except:
		failed.append(i)
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
	'meta_data': [meta_data]
	}
	new_df = pd.DataFrame(new_dataformat)
	final_df = pd.concat([final_df, new_df], axis = 0, ignore_index= True).reset_index(drop=True)
	print(cc)
	cc += 1

final_df.to_csv(f"Taz_complete_data.csv", sep= ";")
print("SUCCESS FILES HAVE BEEN CONVERTED * * *")
# 	#time.sleep(1)
fail = open("failed_taz.txt", "a")
fail.write(str(failed))