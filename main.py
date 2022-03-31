from bs4 import BeautifulSoup
import requests
import uuid
import re
url="https://news.google.com/topics/CAAqJggKIiBDQkFTRWdvSUwyMHZNRGx1YlY4U0FtRnlHZ0pGUnlnQVAB?hl=ar&gl=EG&ceid=EG%3Aar"
allarr=[]
headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)"
                      "Chrome/72.0.3538.102 Safari/537.36 Edge/18.19582"
    }
response = requests.get(url, headers=headers).text
soup = BeautifulSoup(response, 'lxml')
next_page_node = soup.find_all('div',{'jscontroller':"MRcHif"})
print(len(next_page_node))  
for l in next_page_node:
  # print("https://news.google.com"+l.find('a',{'jsname':"hXwDdf"}).get("href"))
  url="https://news.google.com"+l.find('a',{'jsname':"hXwDdf"}).get("href")
  response = requests.get(url, headers=headers).text
  soup = BeautifulSoup(response, 'lxml')
  # print(response)
  # print(soup.find("script",{"type":"application/ld+json"}))
  if soup.find("a",{"jsname":"tljFtd"}).get("href"):
    url=soup.find("a",{"jsname":"tljFtd"}).get("href")
    allarr.append(url)
    string=uuid.uuid4()
    # print(len(soup.find("a")))
    response = requests.get(url, headers=headers).text
    soup = BeautifulSoup(response, 'lxml')
    start=url.find("http://") if url.find("http://")!=-1 else url.find("https://")+1
    t = url[start+11:url.find(" ",start+11)]
    f = open("newHTML1/"+str(len(allarr))+".html", "x")
    ff = open("newHTMLfull1/"+str(len(allarr))+".html", "x")
    # f = open(str(url)+".txt", "x")
    f.write(str(soup.find("script",{"type":"application/ld+json"})))
    ff.write(str(soup))
    f.close()
    ff.close()
print(allarr)