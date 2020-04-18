import requests
from bs4 import BeautifulSoup
import json
import re
HEADERS= {
			"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:70.0) Gecko/20100101 Firefox/70.0",
 			"Accept": "*/*",
  			"Accept-Language": "en-US,en;q=0.5",
   			"Accept-Encoding": "gzip, deflate, br",
    		"Referer": "https://www.google.com/"
    		}
url=r'https://www.rijalsnamkeen.com/'
r = requests.get(url,headers= HEADERS)
soup = BeautifulSoup(r.content,'html.parser')
mails = re.findall("\w+@\w+\.{1}\w+",r.text)
numbers=re.findall("(([+][(]?[0-9]{1,3}[)]?)|([(]?[0-9]{4}[)]?))\s*[)]?[-\s\.]?[(]?[0-9]{1,3}[)]?([-\s\.]?[0-9]{3})([-\s\.]?[0-9]{3,4})",r.text)
nums=[]
for number in numbers:
    num=''.join(number)
    nums.append(num)
links = soup.find_all('a')
fbs = []
for link in links:
    if('.facebook.' in link['href'] or '.fb.' in link['href']):
        fbs.append(link['href'])
print(fbs)
print(nums)
print(mails)
