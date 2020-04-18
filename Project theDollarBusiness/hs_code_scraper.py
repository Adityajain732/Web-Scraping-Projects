from bs4 import BeautifulSoup
def page_scraper(soup):
    Info={}
    features = ['Date','Shipment Id','HS Code','Product description','Buyer country','Buyer','Destination Port','Seller country','Seller','Origin Port','Unit','Quantity','Value(USD)','Unit price']
    if(soup!=None):
        for i in features:
            divs = soup.find_all('div', {'data-label':i})
            data = []
            for j in divs:
                data.append(j.text)
            Info[i]=data
    return Info

def next_page_link(soup):
	if(soup==None):
		return (None,'main soup was empty')
	else:
		link = soup.find('a',{'rel':'next'})
		try:
			if('https://www.thedollarbusiness.com/exim/exim_data/get_company_shipments' in link['href']):
				return (link['href'],'Success')
			else:
				return (None,'link doesnt matches')
		except Exception as e:
			return (None,str(type(e))+str(e))


    
