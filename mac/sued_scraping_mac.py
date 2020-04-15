from bs4 import BeautifulSoup as bs
import time
import os
from datetime import date
import datetime
import simplejson as json
import requests

class SzScraping:

    def __init__(self, link):
        self.sz_html = requests.get(link).text
        self.soup = bs(self.sz_html, 'lxml')
        self.link = link
        self.liste = []
        self.list2 = [] # Die Liste der vollständigen Artikel
        self.let = [] 
        self.html_pages = {}
        self.file = None
        self.Heute = date.today()
        self.link_times_liste = []
        self.link_liste = []

    def show_html(self):
        return print(self.sz_html)

    def show_info(self):
        os.chdir("/Users/Fabi/PycharmProjects/Thesis/ANALYSIS/RaspDTF/Sued_scraping")
        print(" PATH is:", os.getcwd())
        print(" Datum heute ist: ", self.Heute)
        print("")

    def create_json(self): 
        now = datetime.datetime.now()
        datum = now.strftime("%d-%m-%Y")
        try:
            with open(f'{datum}-sued_JSON-{cc}.json', 'r') as fp:
                self.file = json.load(fp)
        except:
            self.file = None
        return self.file

    def find_links(self):
        if self.file:
            self.html_pages.update(self.file)

        for link in self.soup.find_all('a', class_="entrylist__link"):
            if link.has_attr('href'):
                classic = link.attrs['href']
                self.liste.append(link.attrs['href'])
        print(self.liste)
        # time.sleep(100000)
        return self.liste

    def search_links(self):
        i = 0
        for url in self.liste:    
            # while os.path.exists(f"{self.Heute}_art_{i}.html"):
            i += 1
           # REQUEST PART: (sucht nach jedem Einzelnen link in der list)
            print(url)
            article = requests.get(f'{url}').text
            time.sleep(1)
            print(f" Artikel Nummer : {i}")
            if not url in self.html_pages:   # Wird geprüft url in json datei schon drinnen ist
                print("* File is not in json. Replacing it! *")
                self.html_pages[url] = article   # Ersetzt artikel
            else:
                if not self.html_pages[url] == article:
                    self.html_pages.update({url: article})
                    print("* Update html_pages *")

        os.chdir("/Users/Fabi/PycharmProjects/Thesis/ANALYSIS/RaspDTF/Sued_scraping")
        with open(f'{datum}-sued_data-result-{cc}.json', 'w+') as fp:
            json.dump(self.html_pages, fp) # fp = filepointer objekt
        return self.let, self.list2

    def get_links(self):
        index_html = requests.get(self.link).text
        soup = bs(index_html, 'lxml')

        for item in soup.find_all('a', class_="entrylist__link"):
            if item.has_attr("href"):
                link = item.attrs['href']
                self.link_liste.append(link)

        for i in soup.find_all('time', class_="entrylist__time"):
            i1 = i.text
            i2 = i1.replace("\n","")
            i3 = i2.strip()
            self.link_times_liste.append(i3)

        ziped = zip(self.link_liste, self.link_times_liste)
        ziped_list = [i for i in ziped]
        n_ziped_list = []
        for i in ziped_list:
            iii = str(i)
            i1 = iii.replace("(","")
            i2 = i1.replace(")","")
            i3 = i2.replace("\n","")
            i4 = i3.replace('"','')
            i5 = i4.replace("'","")
            n_ziped_list.append(i5)

        os.chdir("/Users/Fabi/PycharmProjects/Thesis/ANALYSIS/RaspDTF/Sued_scraping")
        #os.chdir("/media/pi/datadrive/databank/WELT-SCRAPING/links")
        with open(f'{datum}-suedz_links-{cc}.txt', 'w') as file:
            for element in n_ziped_list:
                file.write(element + "\n")


now = datetime.datetime.now()
datum = now.strftime("%d-%m-%Y")
uhrzeit = now.strftime("%H:%M")
master = 1 
max_days = 14
cc = 1
print(" >>>>>>>>>>>>>>>>>>>> START <<<<<<<<<<<<<<<<<<<<<")
link = 'https://www.sueddeutsche.de/news?search=&sort=time&all%5B%5D=dep&all%5B%5D=typ&sys%5B%5D=sz&sys%5B%5D=dpa&catsz%5B%5D=szOverviewPageThemes&catdpa%5B%5D=alles&time=P1D'
while master <= max_days:
    os.chdir("/Users/Fabi/PycharmProjects/Thesis/ANALYSIS/RaspDTF/Sued_scraping")
    now = datetime.datetime.now()
    datum = now.strftime("%d-%m-%Y")
    print("------>", datum, "---", uhrzeit, "<-------")
    run = SzScraping(link)
    #run.show_html()
    run.show_info()
    run.create_json()
    run.find_links()
    run.search_links()
    run.get_links()
    master += 1
    cc += 1
    now = datetime.datetime.now()
    datum = now.strftime("%d-%m-%Y")
    uhrzeit = now.strftime("%H:%M")
    print(datum, "---", uhrzeit)
    print(" ")
    print(" ... ")
    print(" ")
    print("Going to Sleep ** --> 12 hours zZZ")
    time.sleep(43200)

print(" Alles geklappt, Spitze! 👾👾👾 😁😁 👾👾👾 ")
print("")
print(" ####### * E * N * D * E ######## ")

# Was noch ergänzt werden könnte:

# 1. Abspeichern der Kommentare
#   1.1 Kommentarspalte um alle Anzuzeigen finden um Link zu lokalisieren
#   1.2 Requesten
#   1.3 Write as HTML

# 2. Einzelne Rubriken finde ich mehr Information?

# .prettify()
# 📄 🗞 📰 📑 📃 📜 📯 📆 📅 🗓 📚 📝 🔍 🔎 📌 ⚜️ 🌐 🌀 ✖️ 🕗
