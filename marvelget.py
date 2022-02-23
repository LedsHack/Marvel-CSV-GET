from sre_constants import INFO
from turtle import forward
import requests
from bs4 import BeautifulSoup as BS
import csv

r = requests.get("https://www.marvel.com/characters")
html = BS(r.content, 'html.parser')
get = {}
def get_info(get, st):
    link = "https://www.marvel.com" + get[st]
    name = st
    data = {'name': name, "link": link}
    r = requests.get(link)
    gets = ["Universe", "Other Aliases", "Education", "Place of Origin", "Identity", "Known Relatives"]
    html = BS(r.content, 'html.parser')
    print("INFO! name>  " + name)
    print("INFO! link>  " + link)
    for info in html.select(".accordion-body")[0].select(".railBioInfo > li"):
        for infoget in gets:
            if(infoget in info.text):
                data[infoget] = info.text.split(infoget)[1]
    return data

def get_link(link):
    r = requests.get("https://www.marvel.com" + link)
    html = BS(r.content, 'html.parser')
    print("INFO! getlink> "+ link)

    forward = html.select(".masthead__tabs")[0].select(".masthead__tabs__link")
    #print(forward[len(forward) - 1].get("href"))
    return (forward[len(forward) - 1].get("href"))

for el in html.select('.grid__6 > .mvl-card--explore'):
    no_get = ["/characters/knull"]
    name = el.select('.card-body__headline')[0].text
    #print(name)
    link = el.find_all('a')[0].get('href')
    #print(link)
    if(link not in no_get):
        get[name] = get_link(link)
    #break
    
with open('Marvel.csv', 'w', newline='') as csvfile:
    fieldnames = ["name", "link", "Universe", "Other Aliases", "Education", "Place of Origin", "Identity", "Known Relatives"]
    writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
    writer.writeheader()
    for sset in get.keys():
        writer.writerow(get_info(get, sset))

