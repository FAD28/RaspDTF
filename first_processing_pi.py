################################################################
# READING & TRANSPOSING 
""" Replaces old files with new pd readable frame docs  """

# - FINISHED SCRIPT!
# 1x PATH 
################################################################
from bs4 import BeautifulSoup as bs 
import time, os
import pandas as pd
from txtanalysis import DataCleaner as DC
import datetime, csv

now = datetime.datetime.now()
print(now)
datum = now.strftime('%d-%m-%Y-')

def pre_processing(version):
	os.chdir('/media/pi/datadrive/databank/WELT-SCRAPING/output')
	file = open(version, encoding='utf8')
	data = [i.split() for i in file]
	# ARTIKEL KOMMAS ENTFERNEN
	t = " ".join(data[3])
	i = t.replace(",","")
	data_article = [i.replace('"',"")]
	# SUMMARY
	data_summary = [" ".join(data[2])]
	# TIME
	data_time = [" ".join(data[1])]
	# HEADLINE
	head = " ".join(data[0])
	hh = head.replace('"','')
	data_head = [hh.replace(",","")]

	#column_names = ['headline', 'time', 'summary', 'article']
	df = pd.DataFrame({'headline':data_head, 'time':data_time, 'summary':data_summary,'article':data_article})
	df.to_csv(version)
	print(f"File: {version} was successfully created * * *")

# EXECUTE
y = 1
max_days = 14
while y <= max_days:
    print("DAY NUMBER: ", y, "/", max_days)
    now = datetime.datetime.now()
    print(now)
    datum = now.strftime('%d-%m-%Y-')
    print("_______________________")
    time.sleep(4)
    x = 1
    ini = '03-04-2020'
    #ini = input("Which Date? dd-mm-yyyy ")
    #ml = input("How many files?  ")
    max_loop = 100
    #print("")
    #print("______________________________", ini, "-----")
    while x < max_loop: 
            v_num = str(x)
            var_datum = ini + "-"
            version = var_datum + v_num +'-welt_data' + '.csv'
            print(version)
            try:
                    pre_processing(version)
            except:
                    print("No more Files available.")
            time.sleep(1)
            x += 1
    y += 1
# new_version = datum + str(num) +'-welt_data' + '.csv'
# reading_file(version,num)


def output_processing1(file):
	pass




















