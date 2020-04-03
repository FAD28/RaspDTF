from selenium import webdriver
from bs4 import BeautifulSoup as bs
import requests
import time
import csv
import pandas as pd 
import datetime
from tqdm import tqdm
import itertools
import os

now = datetime.datetime.now()
date = now.strftime("%d-%m-%Y")
zeit = now.strftime("%H:%M")
print("Current date is:", date)
print("")

link = "https://www.taz.de/"

class TazScraping:

	def __init__(self):
		pass

	def get_links(self, link):
		html = requests.get(link).text
		soup = bs(html, "lxml")

		self.all_list = []
		for element in soup.find_all('a',class_="objlink"):
			if element.has_attr("href"):
				link = element.attrs['href']
				self.all_list.append(link)
		# print(self.all_list)
		# print("____________")
		count_links = len(self.all_list)
		print("Links Original:", count_links)

		return self.all_list, count_links

	def clean_links(self):
		links_list = self.all_list
		for item in links_list[:]:
			if item.startswith('/!169313/'):
				links_list.remove(item)

			if item.startswith('https:'):
				links_list.remove(item)

			if item.startswith('/taz-Salon'):
				links_list.remove(item)

			if item.startswith('/Der-taz'):
				links_list.remove(item)

			if item.startswith('/Galerie/'):
				links_list.remove(item)

			if '#matomo' in item:
				links_list.remove(item)

		print("Useful Links =  ",len(links_list))
		os.chdir("/home/peter/Arbeitsfläche/TAZ-SCRAPING/links")    # PATH TO DIRECT
		VERSION_Links = f'{date}_links.txt'
		with open(VERSION_Links, 'w') as file:
			for element in links_list:
				file.write(element + "\n")
		return links_list

	def get_data(self):
		c_success = 0
		c_failed = 0
		cc = 0 
		for i, item in enumerate(links_list):
			print("Durchlauf Nummer: *-----* ", i+1,"/",len(links_list))
			print(item, "* * * *")
			link = str("https://www.taz.de/" + item)
			#time.sleep(160)
			html_article = requests.get(link).text
			cc += 1
			print(cc)
			time.sleep(10)
			if cc == 10:
				print("BREAK- WAITING FOR NEXT 10")
				time.sleep(180)
				cc = 0
			soup = bs(html_article, 'lxml')

			article_list = []
			for item in soup.find_all('p', class_="article"):		# <---- 1.	 DER ARTIKEL
				article = item.text
				article_list.append(article)

			headline = []
			for item in soup.find_all('h1'):					# <----- 2.	 DIE HEADLINE
				head = item.text
				headline.append(head)

			# -----------
			# VERSIONIERUNGS NAME
			""" 
				Vielleicht sollte hier in Zukunft was anderes wie Headline genommen werden damit der Versions Name kürzer wird !
			"""
			print(headline)
			for i in headline:
				x = i.replace(" ","_")
				y = x.replace("-","")
				z = y.replace(":","")
				z1 = z.replace("„","")
				z2 = z1.replace(",","")
				z3 = z2.replace("!","")
				z4 = z3.replace("“","")
				z5 = z4.replace(".","")
				z6 = z5.replace("\n","")
				name_article = z6.lower()
			# ----------

			metatag_liste = []						# <---- 3.	meta Tag META CONTENT.
			for item in soup.find_all('meta'):
				if item.has_attr('content'):
					tt = item.attrs['content']
				metatag_liste.append(tt)

			intro_liste = []
			for item in soup.find_all('p', class_='intro'):		# <---- 4.	p Tag INTRO Das ist die Zusammenfassung unter der Überschrift
				intro = item.text
				#print(intro)

			headline_4_liste = []					# <---- 5.	 h4 Tag HEADLINE 4. Im versuchsartikel war der erste Name der Autor
			for item in soup.find_all('h4'):
				headline_4 = item.text
				headline_4_liste.append(headline_4)

			kommentare_liste = []
			for item in soup.find_all('div', class_='objlink nolead'): 		# <---- 6.	DIE KOMMENTARE
				kommentar = item.text
				kommentare_liste.append(kommentar)

			autor_kommentar_liste = []
			for item in soup.find_all('a', class_='author person'):		# <------ 7. DIE Authoren
				author = item.text
				autor_kommentar_liste.append(author)

			# ------->  VERSIONS NAME <---------

			VERSION= f'{date}-{name_article}.csv'

			def create_output(filename,liste1, liste2, liste3, liste4, liste5, liste6, liste7):
				os.chdir("/home/peter/Arbeitsfläche/TAZ-SCRAPING/output")				# PATH TO DIRECT

				data = {}
				data['headline'] = liste1
				data['article'] = liste2
				data['meta_data'] = liste3
				data['intro_data'] = liste4
				data['h4_data'] = liste5
				data['comments_data'] = liste6
				data['author_data'] = liste7
				df = pd.DataFrame(data.items())
				print(df)
				time.sleep(2)
				df.to_csv(filename, sep=';')
			# VV
			try:
				create_output(VERSION, headline, article_list, metatag_liste, intro_liste, headline_4_liste, kommentare_liste, autor_kommentar_liste)
				print("_______________________________________________________________________________")
				print("OUTPUT CREATED + + + + +  SUCCESS + + + Filename=", VERSION)
				print("TIME IS:", zeit)
				print("_______________________________________________________________________________")
				time.sleep(3)
				c_success += 1
			except:
				print("_______________________________________________________________________________")
				print("OUTPUT FAILED - - - - -  FAILED - - - Filename=", VERSION)
				print("TIME IS:", zeit)
				print("_______________________________________________________________________________")
				c_failed += 1
		print("")
		print(f"FINAL RESULTS: ---> {c_success} SUCCESS")
		print(f" ---> {c_failed} FAILED")
		print("_______________________________________________________________________________")
		print("TIME IS:", zeit)

	def selenium_open(self):
		x = 0
		print(links_list[x])
		time.sleep(3)
		self.driver = webdriver.Chrome(executable_path='/Users/Fabi/Downloads/chromedriver')
		self.driver.get(f'https://www.taz.de/{links_list[x]}')
		time.sleep(5)
		try:
			print("FIRST XPath for nerv_nicht_button ***")
			nerv_nicht_button = self.driver.find_element_by_xpath('//*[@id="tzi-paywahl-fg"]/div/ul[1]/li/a')
		except:
			print("SECOND XPath for nerv_nicht_button ***")
			nerv_nicht_button = self.driver.find_element_by_xpath('//*[@id="tzi-paywahl-fg"]/div/ul/li[2]/a')
		time.sleep(2)
		nerv_nicht_button.click()
		print("Closing all?")
		time.sleep(2)
		try:
			driver.switch_to.window(driver.window_handles[1])
			driver.close()
		except:
			pass
		time.sleep(3)
		x += 1

	def selenium_find_comments(self):
		time.sleep(4)
		try:
			driver.switch_to.window(driver.window_handles[1])
			driver.close()
		except:
			pass
		time.sleep(4)
		for elements in self.driver.find_elements_by_xpath('//div[@class="objlink nolead"]'):
			print(elements.text)
			#//div[@class="objlink nolead"]
			#//*[@id="bb_message_3930674"]/div/p
			#//*[@id="bb_message_3930657"]/div/p
			#//*[@id="bb_message_3930674"]/div
			#//*[@id="pages"]/div[4]/span/div[2]/ul
			# kommentare_list.append(elements.text)

run = TazScraping()
# run.driver_start()
run.get_links(link)
links_list =run.clean_links()
print("_______________________________________________________________________________")
x = 1
while x < 10:
	time.sleep(2)
	run.get_data()
	#run.selenium_open()
	# time.sleep(2)
	#run.selenium_find_comments()
	print("COUNTER: ",x)
	print(f"DATE IS: {date} - - - TIME IS: {zeit}")
	print("Going to Sleep ** --> zZZ")
	time.sleep(86400)
	x += 1

print(" <----> ")
print("PROCESS FINISHED 1")