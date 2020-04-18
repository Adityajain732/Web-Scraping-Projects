#scraper for fetching links and past date and location from pageindex = 1,2,3 ..... and so on
from bs4 import BeautifulSoup

def page_scraper(html):
    Info = {}
    soup = BeautifulSoup(html,'html.parser')
    items = soup.findAll('div',{'class':'col-md-12 list_item'})
    if(not items):
        return Info
    links = []
    dls = []
    for item in items:
        try:
            link = 'https://www.expocheck.com'+item.find('a')['href']
        except:
            link = 'NA'
        try:
            dl = item.find('div',{'class':'col-md-6 col-xs-12 no-padding'}).find('p').text
            dl = " ".join(dl.split())
        except:
            dl = 'NA'
        links.append(link)
        dls.append(dl)

    Info['expo_link']=links
    Info['past_date_and_location']=dls
    return Info
        
                
            
