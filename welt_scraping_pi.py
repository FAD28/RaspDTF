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
			print("SLEEPING FOR 30 SECONDS: ***")
			for i in tqdm(range(30)):
				sleep(1)
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
			# try:
			# 	item1 = name_article[0].replace(",","")
			# except:
			# 	try:
			# 		yo = name_article[0]
			# 		item1 =yo.replace(",","")
			# 	except:
			# 		yo = str(name_article)
			# 		item1 = yo.replace(",","")
			
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
			sleep(10)

	def get_comments_selenium(self):
		driver = webdriver.Chrome(executable_path="/Users/Fabi/Downloads/chromedriver")
		for element in self.soup_links_today:
			link = "https://www.welt.de" + element
			driver.get(link)
			print("Opening Page to Access the comments.... LINK =", link)
			sleep(8)
			try:
				comments_button = driver.find_element_by_xpath('//*[@id="top"]/main/article/div[1]/div[1]/div/div[1]/span/a')
				comments_button.click()
				sleep(5)
				try: 
					umfrage_close = driver.find_element_by_xpath('//*[@id="iam_close"]')
					umfrage_close.click()
				except:
					print("keine Umfrage")
					pass
				sleep(5)
				try:
					more_comments1 = driver.find_element_by_xpath('//*[@id="Comments"]/div/section/div/div[1]/div/div/div[3]/div[1]/div/div[3]/div[2]/a')
					more_comments1.click()
				except:
					# print("no more_comments1")
					pass
				sleep(5)
				try:
					more_comments = driver.find_element_by_xpath('//*[@id="Comments"]/div/section/div/div[1]/div/div/div[3]/div[1]/div[11]')
					more_comments.click()

				except:
					print("no more_comments ...")
					pass
			except:
				print("No comments found on this page")
				continue
			print("Lets hunt the comments :) ")
			print("___________________________________________________________")
			comments = driver.find_elements_by_xpath('//*[@id="Comments"]/div/section/div/div[1]/div/div/div[3]/div[1]')
	
			for elem in comments:
				print(elem.text)
				print("_____")
				sleep(.2)
			print("!!!!")
			sleep(100)
		
	def driver_create_list(self):
		self.article_list = [item.text for item in self.driver.find_elements_by_xpath('//*[@id="top"]/main/article/div[1]')]
		count_word = []
		for item in tqdm(self.article_list):
			count_word.append(item.split())
		print("Anzahl der Wörter:",len(count_word[0]))
		print(self.article_list)
		return self.article_list


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
		
run = WeltScraping()
# run.get_links()

#x = input("Do you have the links to run the script? (y/n)?")
master = 0 



#if x == "y":
print("Aktuelle Uhrzeit ist: ",uhrzeit)
#ml = input("How many Days you want to scrape? ")
max_loop = int(14)

while master <= max_loop:
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
        print("Going to Sleep ** --> zZZ")
        sleep(86400)
# run.get_comments_selenium()  # HABE FESTGESTELLT DAS ICH DAS GARNICHT BRAUCHE WEIL #Comments
# run.driver_start()
# run.driver_create_list()
# run.show_mainpage_text()
# run.show_hfref_attribute()
# run.soup_get_article()
# run.driver.close()
else:
	print("run = WeltScraping()")
	print("get_links()")

	# GETTING THE COMMENTS FROM THE ARTICLE:
	# try:
	# 	comments_count = soup.find('span', class_="c-social-bar__icon-label")
	# 	print(comments_count.text)
	# 	sleep(3)
		
		# for item in soup.find_all('div'):
		# 	if item.has_attr("data-qa"):
		# 		if item.attrs['data-qa'] == "comment":
		# 			print(item.text)
	# except:
	# 	print(" :( commentare konnten nicht gescraped werden")

	# NICHT GEKLAPPT: 
	# for element in self.soup_links_today:
	# 	link = "https://www.welt.de" + element + "#Comments"
	# 	print("LINK =", link)
	# 	comments_html =requests.get(link).text
	# 	soup = bs(comments_html, 'lxml')
	# 	print(soup)
	# 	print("???")
	# 	# sleep(4)
	# 	# for item in soup.find_all('span'):
	# 	# 	print(item.text)
	# 	# 	print("____")
	# 	# 	sleep(.2)

	# 	# for item in soup.find_all('div'):
	# 	# 	if item.has_attr("data-qa"):
	# 	# 		if item.attrs['data-qa'] == "comments":
	# 	# 			print(item.text)
	# 	# print("!!!!")
	# 	# sleep(1000)

# //*[@id="Comments"]/div/section/div/div[1]/div/div/div[3]/div[1]/div[11]/a/span
# //*[@id="Comments"]/div/section/div/div[1]/div/div/div[3]/div[1]/div[11]
# //*[@id="Comments"]/div/section/div/div[1]/div/div/div[3]/div[1]/div[11]/a/span/span/svg
# //*[@id="Comments"]/div/section/div/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/span
# //*[@id="Comments"]/div/section/div/div[1]/div/div/div[3]/div[1]/div[2]/div/div[3]/span
# //*[@id="Comments"]/div/section/div/div[1]/div/div/div[3]/div[1]/div[1]/div/div[3]/span
# //*[@id="Comments"]/div/section/div/div[1]/div/div/div[3]/div[1]/
# //*[@id="Comments"]/div/section/div/div[1]/div/div/div[3]/div[1]/div[10]/div[1]/div[3]/span
