import pandas as pd 
import os, time
from txtanalysis import DataCleaner as DC
from txtanalysis import DataWrangling as DW

os.chdir("/Users/Fabi/PycharmProjects/Thesis/ANALYSIS/Thesis/Zeit_sample")
paths = DW.get_all_paths(os.getcwd())
print("\n".join(paths))

tt = "/Users/Fabi/PycharmProjects/Thesis/ANALYSIS/Thesis/Zeit_sample/9-Coronavirus-Wann-geht-der-Wucher-endlich-offline-06-04-2020-ZEIT.csv"

failed = []
cc = 1
for i in paths:
	datum = i[-19:-4]
	print(datum, "*********************")

	df = open(i)
	dd = [i for i in df]
	nd = []
	for i in dd: 
		i1 = i.replace("\n","")
		i2 = i1.strip()
		i3 = i2.replace('"',"")
		i4 = i3.replace("Bitte melden Sie sich an, um zu kommentieren.","")
		nd.append(i4)

	while("" in nd) : 
	    nd.remove("")

	col_names = nd[0]
	headerkicker = nd[1]
	headline = nd[2]
	author = nd[3]
	try:
		times = nd[4]
	except:
		failed.append(i)
		print("*******************", i, "-----", df)
		continue

	try:
		summary = nd[5]
	except:
		failed.append(i)
		continue
	article = " ".join(nd[6:-1])
	tags = nd[-1]
	versionsname = DC.clean_filename(headline)

	new_df = pd.DataFrame({'headerkicker': [headerkicker], 'headline': [headline], 'time': [times], 'summary': [summary] ,'article': [article], 'author': [author], 'tags': [tags] })
	print(new_df)
	print("________")
	new_df.to_csv(f"{cc}-{versionsname}-{datum}.csv", sep= ";")
	cc += 1 
	#time.sleep(1)
fail = open("failed.txt", "a")
fail.write(str(failed))
