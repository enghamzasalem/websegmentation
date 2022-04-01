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
    h1=soup.find("h1").text
    print(h1)
    articledivs=soup.find("article")
    
    divs=soup.find_all("div")
    i=0
    maxx=1
    alldivs=[]
    print(len(divs))
    for i in divs:
      # print(alldivs)
      # alldivs.append(divs[i].text)
      l=int(len(i))
      if l>maxx:
        body=i.text
        maxx=len(i.text)
        
      #   # print(max)
        # alldivs.append(divs[i].text)
    # print(alldivs)
    # print(alldivs)
    # hi = max(alldivs) 
    # max = max(divs, key=len)
    # max_length,longest_element = max([(len(x),x) for x in alldivs ])
    print(maxx)
    print(body)
    # start=url.find("http://") if url.find("http://")!=-1 else url.find("https://")+1
    # t = url[start+11:url.find(" ",start+11)]
    fn = open("newHTMLinjected4/"+str(len(allarr))+".json", "x")
    if articledivs is not None:
      description = soup.find("meta",{'name':'description'})
      token=url.split('https://')[1].split('/')[0]
      top_level=token.split('.')[-2]+'.'+token.split('.')[-1]
      jsonID={
                    "@context": "https://schema.org",
                    "@type": "WebPage",
                    "name": h1,
                    "description":  description.get("content"),
                    "publisher": {
                        "@type": "Organization",
                        "name": soup.title.get_text().split("|")[-1],
                        "url": top_level,
                        "alternateName": soup.title.get_text().split("|")[-1],
                        "logo": {
                            "@type": "ImageObject",
                            "url": "https://www.skynewsarabia.com/icon.png",
                            "width": 192,
                            "height": 192
                        }
                    },
                    "identifier": url,
                    "url":url
                }
      fn.write(str(jsonID))
      fn.close()
    # f = open("newHTML1/"+str(len(allarr))+".html", "x")
    # ff = open("newHTMLfull1/"+str(len(allarr))+".html", "x")
    # # f = open(str(url)+".txt", "x")
    # f.write(str(soup.find("script",{"type":"application/ld+json"})))
    # ff.write(str(soup))
    # f.close()
    # ff.close()
print(allarr)