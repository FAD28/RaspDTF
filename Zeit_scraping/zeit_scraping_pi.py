from bs4 import BeautifulSoup as bs
import time
import os
from datetime import date
import simplejson as json
import requests

class ZeitScraping:

    def __init__(self):
        self.zeit_html = requests.get(link).text
        self.soup = bs(self.zeit_html, 'lxml')
        self.a = ["classic", "wide", "standard"]
        self.liste = []
        self.list2 = [] # Die Liste der vollständigen Artikel
        self.let = [] 
        self.html_pages = {}
        self.file = None
        self.Heute = date.today()

    def show_html(self):
        return print(self.zeit_html)

    def show_info(self):
        os.chdir("/media/pi/datadrive/databank/ZEIT-SCRAPING/output")
        print(" PATH is:", os.getcwd())
        print(" Datum heute ist: ", self.Heute)
        print("")

    def create_json(self):    
        try:
            with open('result.json', 'r') as fp:
                self.file = json.load(fp)
        except:
            self.file = None
        return self.file

    def find_links(self):
        if self.file:
            self.html_pages.update(self.file)

        for value in self.a:
            for link in self.soup.find_all('a', class_=f"zon-teaser-{value}__combined-link"):
                if link.has_attr('href'):
                    classic = link.attrs['href']
                    self.liste.append(link.attrs['href'])
        print(self.liste)
        return self.liste

    def search_links(self):
        i = 0
        for url in self.liste:    
            # while os.path.exists(f"{self.Heute}_art_{i}.html"):
            i += 1
           # REQUEST PART: (sucht nach jedem Einzelnen link in der list)
            article = requests.get(f'{url}').text
            time.sleep(0.2)
            print(f" Artikel Nummer : {i}")
            if not url in self.html_pages:   # Wird geprüft url in json datei schon drinnen ist
                print("* File is not in json. Replacing it! *")
                self.html_pages[url] = article   # Ersetzt artikel
            else:
                if not self.html_pages[url] == article:
                    self.html_pages.update({url: article})
                    print("* Update html_pages *")

        print("---> KOMPLETTE LINKS <---")
        soup2 = bs(self.article, 'lxml')
        for linki in soup2.find_all('a', class_='article-toc__onesie'):
            if linki.has_attr('href'):
                classic = linki.attrs['href']
                # print(classic)
                print(f"KOMPLETTER LINK GEHÖRT ZU: {i} 😸")
                print("")
                self.let.append(i) # Hinzufügen der Nummerierung des vollständigen Artikel in let
                self.list2.append(linki.attrs['href']) # Hinzufügen der Links in list 2

        os.chdir("/media/pi/datadrive/databank/ZEIT-SCRAPING/links")
        with open('result.json', 'w+') as fp:
            json.dump(self.html_pages, fp) # fp = filepointer objekt
        return self.let, self.list2

    def write_output(self):
        os.chdir("/media/pi/datadrive/databank/ZEIT-SCRAPING/output")
        for url2 in self.list2:
            k = 1
            while os.path.exists(f"{self.Heute}_comp_art_{k}.html"):
                k += 1

            f1 = open(f"{self.Heute}_comp_art_{k}.html", "w+")

           # REQUEST 2. PART: (sucht nach jedem vollständigen Artikel in list 2)
            article1 = requests.get(f'{url2}').text
            print(f"Vollständiger Artikel Nr. {k} --> Zugehörige Artikel Nr.: {self.let}")
            # print(article1)
            time.sleep(0.25)
            f1.write(article1)
            time.sleep(0.25)
            f1.close()

    def write_txt(self):
        """ Funktion die in einem txt file die kompletten abspeichert"""
        let_file = open(f'{self.Heute}_COMPLETE_LOG.csv', "w+")
        let_file.write(str(self.let))
        let_file.close()

    def print_info(self):
        print("")
        print(" Nummerierungen bei der vollständige Artikel gefunden wurden:")
        print(f" Die Nummerierungen sind {self.let}")
        print("")
        print("********************************")
        print("**** JETZT VOLLSTÄNDIGE ARTIKEL ****")
        print("********************************")
        print("##### Liste 2 erzeugen: #####")
        print(self.list2)
        print(" ####### * * * ####### ")
        print("")
        print(" ####### * * * ####### ")
        print("")
        print(" Output: ")
        print(f" Artikel heißen jetzt: '{self.Heute}_art_1.html' & '{self.Heute}_comp_art_1.html'")
        print("")
        print(f" Achtung (!!!) entsprechen nicht der selben Artikelnummerierung.")
        print("")
        print(" Siehe hierzu Liste:")
        print(f" --> {self.let} <-- ")
        print("")

master = 1 
max_days = 14
print(" >>>>>>>>>>>>>>>>>>>> START <<<<<<<<<<<<<<<<<<<<<")
link = "https://www.zeit.de/index"
while master <= max_days:
    os.chdir("/media/pi/datadrive/databank/ZEIT-SCRAPING/output")
    run = ZeitScraping()
    run.show_html()
    run.show_info()
    run.create_json()
    run.find_links()
    run.search_links()
    run.write_output()
    run.write_txt()
    master += 1
    print(" ")
    print(" ... ")
    print(" ")
    print("Going to Sleep ** --> zZZ")
    sleep(86400)

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