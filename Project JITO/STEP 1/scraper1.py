#scraper for fetching profile links from pageindex = 1,2,3 ..... and so on
from bs4 import BeautifulSoup

def page_scraper(html):
	Info = {}
	links = []
	soup = BeautifulSoup(html,'html.parser')
	divs = soup.findAll('div',{'class':'mini-profile-avatar'})
	if(not divs):
		return Info
	for div in divs:
		try:
			links.append('https://jito.org'+div.find('a')['href'])
		except:
			pass
	Info['profile link'] = links
	return Info
