###############################################################################################
#    			PI- 		VERSION
#



##############################################################################################
import pandas as pd 
from time import sleep
import os
import requests
from bs4 import BeautifulSoup as bs
import datetime

class Functions:
	def __init__(self):
		self.remove_me = '/media/pi/datadrive/databank/WELT-SCRAPING/RaspDTF/Welt_scraping/remove_me_welt.csv'
		self.rm = pd.read_csv(self.remove_me, header = None)
		self.rm_list = list(self.rm[0])
		self.output = []
		self.link_liste = []
		self.article_names = []

	def article_clean(self, data, headline, time, summary, article, new_version_number):	
		os.chdir('/media/pi/datadrive/databank/WELT-SCRAPING/output')
		for i in data: 
			ii = i.strip()
			if ii not in self.rm_list:
				if ii.startswith("Quelle:"):         # DAS HIER KÖNNTE NÜTZLICH SEIN UM DIE QUELLEN IN DEN ARTIKELN NOCHMAL GESONDERNT ZU SAMMELN
					print("Quellen-info = ", ii)
					continue
				if ii.startswith("“  Quelle"):
					continue
				if ii.startswith('de/'):			# DAS HIER KÖNNTE NÜTZLICH SEIN UM DEN LINK WIEDER ZU FINDEN ZU DEM DER ARTIKEL GEHÖRT
					print("link Nummer: ", ii)
					self.link_liste.append(ii + f"- ART- NUMBER- {number}")
					continue
				self.output.append(ii)

		self.new_data(headline, time, summary, article, new_version_number)

		return self.output, self.link_liste

	def new_data(self, liste0, liste1, liste2, liste3, version_name):
		# PATH TO OUTPUT
		os.chdir('/media/pi/datadrive/databank/WELT-SCRAPING/processing_out')
		df= pd.DataFrame({'headline': liste0, 'time': liste1, 'summary': liste2, 'article': liste3})
		print(df)
		print(" ---->   ",version_name)
		df.to_csv(version_name)

	def clean_name(self, name):
		new_list= []
		for i in name:
			i1 = i.replace(".","")
			i2 = i1.replace("-","")
			i3 = i2.replace(" ","-")
			i4 = "".join(i3)
			i5 = i4.replace('–',"")
			i6 = i5.replace('„','')
			i7 = i6.replace('“','')
			i8 = i7.replace("?",'')
			i9 = i8.replace("!",'')
			i10 = i9.replace("€",'')
			i11 = i10.replace("(",'')
			i12 = i11.replace(")",'')
			new_list.append(i12)
		nn= "_".join(new_list)
		return nn

run = Functions()
master = 1

#ini = input("Which Date? dd-mm-yyyy ")
#ml = input("How many Artikels? ")

y = 1
max_days = 14
while True:
	print("START: *_*  DAY: ", y )
	now = datetime.datetime.now()
	datum = now.strftime('%d-%m-%Y')
	print("START: * _ * ", datum)
	print("DAY NUMBER: ", y, "/", max_days)
	max_loop = int(100) 
	c = 1
	lo = 1
	ll = str(lo)
	v_list = []
	for i in range(max_loop):
		os.chdir('/media/pi/datadrive/databank/WELT-SCRAPING/output')
		number = str(c)
		version = f'{datum}-{number}-welt_data.csv'
		print("VERSIONS NUMMER:  ",version)
		print("___________________________________")
		try:
			df = pd.read_csv(version)
		except:
			print("FINISHED OR ERROR BY READING")
			continue
		article = df['article']
		time = list(df['time'])
		summary = list(df['summary'])
		hd = df['headline']
		headline = [i for i in hd]

		# New Article Name:
		name = headline[0]
		try:
			name2 = name.split()
			nn = run.clean_name(name2)
			new_version_number = number + "-" + nn + '-' + datum + ".csv"
		except:
			new_version_number = number + "-" + 'NAN' + datum + ".csv"
		v_list.append(new_version_number)
		try:  # TRY: Weil bei Artikeln ohne Inhalt sonst ein Fehler kommt
			data = [i.split(".") for i in article][0]
		except:
			print(" - - - VERSION: {version}   hat einen Fehler. Möglicherweiße kein Inhalt?!")
			c += 1
			continue
		# EXCECUTE
		output, link_liste = run.article_clean(data, headline, time, summary, article, new_version_number)

		sleep(1)
		c += 1

		print("___________________________________")
	print("SUCCESS DATA CONVERTED * * *")
	f = open(f'{ll}-versionsnamen_liste-{datum}.txt', 'w')
	f.write(str(v_list))
	y += 1
	print("Going to Sleep *_* --> 24 hours zZZ")
	sleep(86400)
	










