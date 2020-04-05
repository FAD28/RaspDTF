from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
from time import sleep
import csv
import pandas as pd 
import datetime
from tqdm import tqdm
import itertools, re
import os

now = datetime.datetime.now()
date = now.strftime("%d-%m-%Y")
uhrzeit = now.strftime("%H:%M")
print("Current date is:", date)
print("Current time is:", uhrzeit)
sleep(5)

class WeltScraping:

	def __init__(self):
		self.link = 'https://www.welt.de/'
		self.soup_article_liste = []
		self.soup_links_today = []
		self.todays_links_clean = f'Welt_scraping_LINKS_{date}_clean.txt'
		self.todays_links = f'Welt_scraping_LINKS_{date}.txt'
		self.counter = 1

	def get_links(self):
		'''' Just use it once'''
		print("GETTING THE LINKS ON THE PAGE FOR 24 Hours")
		page_html = requests.get(self.link).text
		soup = bs(page_html, 'lxml')
		for item in soup.find_all('a', class_="o-link o-teaser__link o-teaser__link--is-headline"):
			if item.has_attr("href"):
				link = item.attrs['href']
				self.soup_article_liste.append(link)
		print(self.soup_article_liste)
		os.chdir("/media/pi/datadrive/databank/WELT-SCRAPING/links")
		with open(self.todays_links, 'w') as file:
			for element in self.soup_article_liste:
				file.write(element + "\n")
		return self.soup_article_liste

	def modify_links(self):
		os.chdir("/media/pi/datadrive/databank/WELT-SCRAPING/links")
		links_file = open(self.todays_links, 'r')
		stuff_das_weg_muss = ['/tv-programm-n24-doku/','/videos/','/mediathek/dokumentation/','/mediathek/reportage/','/mediathek/magazin/','/mediathek/moderator/','/mediathek/sendungen-a-z/', '/kmpkt/', '/debatte/','/newsticker/','/','/themen/','/autor/']
		for item in links_file: 
			item1 = item.replace("\n","")
			item2 = item1.replace("/tv-programm-live-stream/","")
			if item2.startswith("/icon/"):
				continue
			if item2.startswith("https://"):
				continue
			if item2.startswith("http://"):
				continue
			if item2.startswith("/apps/"):
				continue
			if "plus" in item2:
				continue
			if item2.startswith("/spiele/"):
				continue
			if item2 in stuff_das_weg_muss:
				continue
			if item2.startswith("/services/"):
				continue
			if item2.startswith("/meinewelt/"):
				continue
			else: 
				self.soup_links_today.append(item2)			# <------------------------- ! ! ! 

		print("000000000000000000000000000000000000000000000000000")
		for item in self.soup_links_today:
			print(item)
		print("GESAMTANZAHL DER LINKS NACH DER ERSTELLUNG UND VERARBEITUNG=", len(self.soup_links_today))
		with open(self.todays_links_clean, 'w') as file:
			for element in self.soup_links_today:
				file.write(element + "\n")
		print("ooooooooooooooooooooooooooooooooooooooooooooooooooo")
		return self.todays_links_clean

	def scrape_articles(self):
		#test_file = open('replace_me.txt', 'r') # TEST
		# HIER WERDEN DIE ARTIKEL GESCRAPED UND DAS IST DER FOR-LOOP DER ALLES MACHT
		for element in self.soup_links_today: #test_file 
			""" HIER MUSS DER ARTIKEL SELBST GESCRAPED WERDEN """
			link = "https://www.welt.de" + element
			print("LINK =", link)
			try:
				article_html =requests.get(link).text
			except:
				print("Eventuell gibt es den link nichtmehr")
				continue
			sleep(2)
			soup = bs(article_html, 'lxml')

			name_article = [item.text for item in soup.find_all('h1', class_='c-breadcrumb__element c-breadcrumb__title')]
			#name_article = [item.text for item in soup.find_all('h2', class_="c-headline o-dreifaltigkeit__headline o-headline--is-emphasis rf-o-headline")]
			print(name_article)
			print(len(name_article))
			try:
				item1 = name_article[0]
				print("TRY 1 -------------------")
			except:
				item1 = name_article 
				print("EXCEPT 0 -------------------")
			try:	
				item2 = item1[0].replace(",","")
				item3 = item2.replace(" ","_")
				item4 = item3.replace(".","")
				name_article = item4
			except:
				name_article = 'FAIL_403'
			
			print(name_article)
			print("::::::")

			headline_list = []
			for headline_item in soup.find_all("h2"):
				headline = headline_item.text
				print("HEADLINE = ", headline)
				headline_list.append(headline)

			print("++++++++++++++++++++++++++++++++++")

			time_list = []
			for time_item in soup.find_all("time", class_="c-publish-date"):
				time = time_item.text
				print("TIME = ", time)
				time_list.append(time)

			print("++++++++++++++++++++++++++++++++++")

			# ALLE Summary_intro
			summary_list = [] 
			for summary_item in soup.find_all('div', class_="c-summary__intro"):
				summary = summary_item.text
				#print("Summary=", summary)
				print("________")
				summary_list.append(summary)

			print("++++++++++++++++++++++++++++++++++")

			# ALLE P-TAGS 
			article_list = []
			for article_item in tqdm(soup.find_all(['p','h3'])):
				article = article_item.text
				print(article)
				print("_______")
				article_list.append(article)
				sleep(.1)

			def create_output(liste1, liste2, liste3, liste4):
				os.chdir("/media/pi/datadrive/databank/WELT-SCRAPING/output")
				#print(" NEW PATH is:", os.getcwd())
				
				with open(f'{date}-{self.counter}-welt_data.csv','w') as f: 
					writer = csv.writer(f)
					writer.writerow(liste1)
					writer.writerow(liste2)
					writer.writerow(liste3)
					writer.writerow(liste4)
				self.counter += 1
			create_output(headline_list, time_list, summary_list,article_list)
			sleep(5)


	def show_mainpage_text(self):
		for item in self.soup.find_all('a', class_="o-link o-teaser__link o-teaser__link--is-headline"): #class_=''
			print(item.text)
			mainpage_text = item.text

	def show_hfref_attribute(self):
		for item in self.soup.find_all('a'):
			if item.has_attr("href"):
				link = item.attrs['href']
				print(link)

	def soup_get_article(self):
		article_1 = self.soup.find_all('div')

		for item in self.soup.find_all('span', class_="frage"):
			self.soup_article_liste.append(item.text)

		for item in self.soup.find_all('span', class_="antwort"): #c-sticky-container
			self.soup_article_liste.append(item.text)

		print(" soup_article_liste erstellt *** ")
		count_word1 = []
		for item in self.soup_article_liste:
			count_word1.append(item.split())
		count_word = list(itertools.chain.from_iterable(count_word1))
		print("Anzahl der Wörter:", len(count_word))

		return self.soup_article_liste

	def create_output(self):
		pass
		
print("Aktuelle Uhrzeit ist: ",uhrzeit)
max_loop = int(14)
master = 1 
while master <= max_loop:
	run = WeltScraping()
	now = datetime.datetime.now()
	date = now.strftime("%d-%m-%Y")
	uhrzeit = now.strftime("%H:%M")
	print("Current date is:", date)
	print("Current time is:", uhrzeit)
	run.get_links()
	run.modify_links()
	run.scrape_articles()
	print("Aktuelle Uhrzeit ist: ",uhrzeit)
	print("DAY NUMBER, ----->", master, " - SUCCESS")
	master += 1
	print(" ")
	print(" ... ")
	print(" ")
	print("Going to Sleep ** --> 24 hours zZZ")
	sleep(86400)
