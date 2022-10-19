from bs4 import BeautifulSoup
import requests
import uuid
from difflib import SequenceMatcher
import json
import csv
import datetime
import os
# today = date.today()
today = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
# print(time_stamp)
# open the file in the write mode

isExist = os.path.exists(str(today))
print(isExist)
if (isExist == False):
    os.makedirs(str(today))
# create the csv writer
bf = open(str(today) + '/' + str(today) + '.csv', 'w')
writer = csv.writer(bf)
writer.writerow([
    "description Old", "description New ", "similarity", "Title New",
    "Title Old", "similarity"
])

# write a row to the csv file

url = "https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtRnlHZ0pGUnlnQVAB?hl=ar&gl=EG&ceid=EG%3Aar"
allarr = []
headers = {
    "User-Agent":
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
    "Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
}
response = requests.get(url, headers=headers).text
soup = BeautifulSoup(response, 'lxml')
next_page_node = soup.find_all('div', {'jscontroller': "MRcHif"})
# print(len(next_page_node))
for l in next_page_node:
    # print("https://news.google.com"+l.find('a',{'jsname':"hXwDdf"}).get("href"))
    url = "https://news.google.com" + l.find('a', {
        'jsname': "hXwDdf"
    }).get("href")
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    # print(response)
    # print(soup.find("script",{"type":"application/ld+json"}))
    if soup.find("a", {"jsname": "tljFtd"}).get("href"):
        url = soup.find("a", {"jsname": "tljFtd"}).get("href")
        allarr.append(url)
        # print(url)
        string = uuid.uuid4()
        # print(len(soup.find("a")))
        response = requests.get(url, headers=headers).text
        soup = BeautifulSoup(response, 'lxml')
        if soup.find("h1"):
            h1 = soup.find("h1").text
        else:
            h1 = '--'
        # print(h1)
        articledivs = soup.find("article")

        divs = soup.find_all("div")
        i = 0
        maxx = 1
        alldivs = []
        # print(len(divs))
        for i in divs:
            l = int(len(i))
            if l > maxx:
                body = i.text
                maxx = len(i.text)
        fn = open(str(today) + "/New" + str(len(allarr)) + ".json", "x")
        if articledivs is not None:
            description = soup.find("meta", {'name': 'description'})
            # token=url.split('https://')[1].split('/')[0]
            # top_level=token.split('.')[-2]+'.'+token.split('.')[-1]
            # print(top_level)
            jsonID = {
                "@context": "https://schema.org",
                "@type": "WebPage",
                "name": h1,
                "description": description.get("content"),
                "publisher": {
                    "@type": "Organization",
                    "name": soup.title.get_text(),
                    # "url": top_level,
                    "alternateName": soup.title.get_text(),
                    "logo": {
                        "@type": "ImageObject",
                        "url": "https://www.skynewsarabia.com/icon.png",
                        "width": 192,
                        "height": 192
                    }
                },
                "identifier": url,
                "url": url
            }
            fn.write(str(jsonID))
            fn.close()
            if (soup.find("script", {"type": "application/ld+json"})):
                json_orignal = soup.find("script", {
                    "type": "application/ld+json"
                }).text
                # print(json_orignal)
                json_orignal = json.loads(json_orignal, strict=False)
                # print(json_orignal)
                # print(json_orignal['description'])
                # print(json_orignal.keys())
                if ('description' in json_orignal.keys()
                        and description.get("content")
                        and 'name' in json_orignal.keys() and h1):
                    text1 = json_orignal['description']
                    text2 = description.get("content")
                    m = SequenceMatcher(None, text1, text2)
                    m.ratio()
                    text3 = json_orignal['name']
                    text4 = h1
                    m2 = SequenceMatcher(None, text3, text4)
                    m2.ratio()
                    print(m2.ratio())
                    writer.writerow(
                        [text1, text2,
                         m.ratio(), text3, text4,
                         m2.ratio()])

                f = open(str(today) + "/Old" + str(len(allarr)) + ".json", "x")
                # ff = open("newHTMLinjected00/"+str(len(allarr))+".html", "x")
                # f = open(str(url)+".txt", "x")
                f.write(str(json_orignal))
                # ff.write(str(soup))
                f.close()
                # ff.close()

        # print(allarr)

    # close the file
bf.close()
