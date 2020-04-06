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
os.chdir("/media/pi/datadrive/databank/ZEIT-SCRAPING/links")

class ZeitParsing:

    def __init__(self):
        self.counter = 1

    def main(self):
        os.chdir("/media/pi/datadrive/databank/ZEIT-SCRAPING/links")
        with open(f'{datum}-Zeit_JSON-{cc}.json', 'r') as fp:
            file = json.load(fp)

        for value in file.values(): # items() gibt immer key-value paare zurück.
            soup = bs(value, 'lxml')
            head_article = soup.find('article')
            article_liste = []
            summary_liste = []
            artheading_kicker_liste = []
            time_liste = []
            keywords_list = []

            # ARTIKEL 
            for i in soup.find_all('p'):
                article_liste.append(i.text)

            # SUMMARY
            for i in soup.find_all('div', class_='summary'):
                summary_liste.append(i.text)

            # HEADING kicker
            for i in soup.find_all('span', class_="article-heading__kicker"):
                artheading_kicker_liste.append(i.text)

            # TIME 
            for i in soup.find_all('time', class_= 'metadata__date'):
                time_liste.append(i.text)

            # KEYWORDS
            for i in soup.find_all('ul', class_='article-tags__list'):
                keywords_list.append(i.text)

            #print(f"Headline:")
            try:
                headline = head_article.h1.text      
            except:
                print("* Keine Überschrift wurde gefunden *")
                pass
            try:
                author = soup.find('div', class_='byline').span.text
            except:
                pass
            colnames = ['headerkicker','headline','author','time', 'summary', 'article','tags']
            
            headline_liste = [headline]
            author_liste = [author]
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

            v_name = clean_name(headline_liste)
            def create_output(colnames_liste, liste1, liste2, liste3, liste4, liste5, liste6, liste7):
                    os.chdir("/media/pi/datadrive/databank/ZEIT-SCRAPING/output")
                    #print(" NEW PATH is:", os.getcwd())
                    now = datetime.datetime.now()
                    datum = now.strftime("%d-%m-%Y")

                    with open(f'{self.counter}-{v_name}-{datum}-ZEIT.csv','w') as f: 
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
            print(f"SUCCESS *_*   file name = {self.counter}-{v_name}-{datum}-ZEIT.csv successfully created :) ")
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
    print("Going to sleep *_* zZZ")
    time.sleep(86400)
print("##################################")



# i = 0
# # while os.path.exists(f"{Heute}_comp_art_{i}.html"):
# while i < 11:
#     i += 1
#     f = open(f'{Heute}_comp_art_{i}.html', 'r').read()
#     print(f'{Heute}_comp_art_{i}.html * wurde geladen *')
#     print("------------------------------------------")
#     soup = bs(f, 'lxml')
#     article = soup.find('article')
#     print(f"Headline/1 :  {i}")
#     try:
#         headline = article.h1.text
#         print(headline)
#     except:
#         print("* Keine Überschrift wurde gefunden *")
#         pass

#     try:
#         author = soup.find('div', class_='byline').span.text
#         print(author)
#     except:
#         pass

#     print("")
#         # author2 = soup.find('div', class_="article-header__byline").span.text
#     try:
#         author2 = soup.find('div', class_="article-header__byline").span.text
#         # print(author)
#         print(author2)
#     except:
#         pass

#     tags = soup.find("nav", class_="article-tags").ul.text
#     print("Tags:")
#     print(tags)


#     print("")
#     print("---")
#     time.sleep(1)
#     # print(type(f))

# print("############################################")
# print("")
# print("")
# print("############################################")
# time.sleep(5)

# print(os.listdir('/Users/Fabi/PycharmProjects/Samples'))

# j = 1
# for filename in os.listdir('/Users/Fabi/PycharmProjects/Samples'):

#     if filename.endswith('.html') and filename.startswith(f"{Heute}_art"):

#         file = open(filename, 'r').read()
#         print(f'{Heute}_art_{j}.html' == filename)
#         print(f'{Heute}_art_{j}.html')
#         print(filename)
#         print("------------------------------------------")
#         soup2 = bs(file, 'lxml')
#         article2 = soup2.find('article')
#         print(f"Headline/2 :  {j}")
#         print("")
#         try:
#             headline2 = article2.h1.text
#             print(headline2)
#         except:
#             print("* Keine Überschrift wurde gefunden *")
#             pass

#         try:
#             author = soup2.find('div', class_='byline').span.text
#             print(author)
#         except:
#             pass
#             # author2 = soup.find('div', class_="article-header__byline").span.text
#         try:
#             author2 = soup2.find('div', class_="article-header__byline").span.text
#             # print(author)
#             print(author2)
#         except:
#             pass
#         print("")
#         print("---")
#         time.sleep(1)
#         j +=1
#         # tags = soup2.find("nav", class_="article-tags").ul.text
#         # print("Tags:")
#         # print(tags)

time.sleep(3)
print("")
print(" Alles geklappt, Spitze! 👾👾👾 😁😁 👾👾👾 ")
print("")
print(" ####### * E * N * D * E ######## ")



# span class_="article-heading__title"

  # for article in soup.find_all("div"):
    #     headline= article.find('span', class_="article-heading__title").text
    #     print(headline)
