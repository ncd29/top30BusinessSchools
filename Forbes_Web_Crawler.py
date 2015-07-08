import requests
import urlparse
import urllib
from bs4 import BeautifulSoup

#helper function
#l is a list, url is optional url text to add if needed
# appendTo is a list to append the links to
def combineURL(l,appendTo,url = "",seperator = ">"):
    for link in l:
        index = link.find(seperator)
        link = url + link[9:index]
        appendTo.append(link)

def getLinks():
    request = requests.get("http://www.forbes.com/business-schools/list/")
    soup = BeautifulSoup(request.content)
    
    #get all the links to the business school pages on Forbes
    links = soup.find_all("a")
    listOfLinks = []
    for item in links:
        link = "<a href='%s>%s</a>" %(item.get("href"), item.text)
        listOfLinks.append(link)
    
    # links to visit
    listOfLinks = listOfLinks[46:76]
    
    urls = []
    combineURL(listOfLinks,urls,"http://forbes.com")
    
    #print urls
    
    # visit each school and get the link to that schools webpage
    eduLinks = []
    while len(urls) > 0:
        page = requests.get(urls[0])
        content = BeautifulSoup(page.content)
        urls.pop(0)
        
        data = content.find_all("ul",{"class":"address"})
        for item in data:
            links = item.find_all("a")
            for item in links:
                link = "<a href='%s>%s</a>" %(item.get("href"), item.text)
                if "edu" in link:
                    eduLinks.append(link)
    
    reducedLinks = []
    for link in eduLinks:
        start = link.index("=")
        end = link.index(">")
        reducedLink = link[start+2:end]
        reducedLinks.append(reducedLink)
    
    return reducedLinks
        



    
