from bs4 import BeautifulSoup as bs
import time
import os, datetime
from datetime import date
import json
import pandas as pd 
import csv


now = datetime.datetime.now()
datum = now.strftime("%d-%m-%Y")

print("")
os.chdir("/media/pi/datadrive/databank/SUED-SCRAPING/links")

class ZeitParsing:

    def __init__(self):
        self.counter = 1

    def main(self):
        os.chdir("/media/pi/datadrive/databank/SUED-SCRAPING/links")
        with open(f'07-04-2020-sued_data-JSON-1.json', 'r') as fp:
            file = json.load(fp)

        for key, value in file.items(): # items() gibt immer key-value paare zurück.
            print(key)
            soup = bs(value, 'lxml')
            head_article = soup.find('article')
            headline_liste =[]
            article_liste = []
            author_liste = []
            summary_liste = []
            artheading_kicker_liste = []
            time_liste = []
            keywords_list = []

            # ARTIKEL check
            for i in soup.find_all('p', class_='css-0'):
                article_liste.append(i.text)

            # SUMMARY

            for i in soup.find_all('div', class_='sz-article__intro css-1pagoky'): #'div', class_='css-13lgcsh'
                summary_liste.append(i.text)

            # HEADING kicker
            for i in soup.find_all('h2', class_="css-1keap3i"):
                artheading_kicker_liste.append(i.text)

            # TIME 
            for i in soup.find_all('time', class_= 'css-11lvjqt'):
                time_liste.append(i.text)

            # KEYWORDS
            for i in soup.find_all('a', class_='css-18b1142'):
                keywords_list.append(i.text)

            # HEADLINE
            try:
                for i in soup.find_all('h1'):
                    headline_liste.append(i.text)    
            except:
                print("* Keine Überschrift wurde gefunden *")
                pass

            # AUTHOR
            try:
                for i in soup.find_all('a', class_='css-viqvuv'):
                    author_liste.append(i.text)
            except:
                pass
            colnames = ['headerkicker','headline','author','time', 'summary', 'article','tags']
            
            print("__________HEADLINE________")
            print(headline_liste)
            print("________ARTIKEL_____")
            print(article_liste)
            print("______SUMMARY______")
            print(summary_liste)
            print("______TAGS_______")
            print(keywords_list)
            print("_______TIME_______")
            print(time_liste)
            print("_______AUTHOR_________")
            print(author_liste)

            time.sleep(1)

            def clean_name(name):
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
                    i13 = i12.replace("/","")
                    i14 = i13.strip()
                    i15 = i14.replace(":","")
                    i16 = i15.replace(",","")
                    i17 = i16.replace('"',"")
                    i18 = i17.replace("'","")
                    i19 = i18.replace("\n","")
                    i20 = i19.replace("»","")
                    i21 = i20.replace("«","")
                    new_list.append(i21)
                nn= "_".join(new_list)
                return nn

            def clean_article(article_liste):
                ohne_commas = []
                for x in article_liste:
                    x1 = x.replace(",","")
                    ohne_commas.append(x1)
                return ohne_commas

            article_liste = clean_article(article_liste)
            print(article_liste)
            v_name = clean_name(headline_liste)
            def create_output(colnames_liste, liste1, liste2, liste3, liste4, liste5, liste6, liste7):
                    os.chdir("/media/pi/datadrive/databank/SUED-SCRAPING/output")
                    #print(" NEW PATH is:", os.getcwd())
                    
                    with open(f'{self.counter}-{v_name}-{datum}-SUED.csv','w') as f: 
                        writer = csv.writer(f)
                        writer.writerow(colnames_liste)
                        writer.writerow(liste1)
                        writer.writerow(liste2)
                        writer.writerow(liste3)
                        writer.writerow(liste4)
                        writer.writerow(liste5)
                        writer.writerow(liste6)
                        writer.writerow(liste7)
                    self.counter += 1
            create_output(colnames, artheading_kicker_liste, headline_liste , author_liste, time_liste, summary_liste, article_liste, keywords_list )
            print(f"SUCCESS *_*   file name = {self.counter}-{v_name}-{datum}-SUED.csv successfully created :) ")
            time.sleep(1)
            #df = pd.DataFrame({'headerkicker': artheading_kicker_liste, 'headline': headline, 'author': author, 'time': time_liste,'summary':summary_liste, 'article':article_liste, 'tags':keywords_list })
            #print(df)
            #print(df.keys())
master = 1
max_days = 14
cc = 1
print(" START:", datum)
while master <= max_days:
    print(f"DAY NUMBER: {master} / 14")
    run = ZeitParsing()
    run.main()
    master += 1
    cc += 1 
    print("Going to sleep *_* --> 24 hours zZZ")
    time.sleep(86400)
print("##################################")
