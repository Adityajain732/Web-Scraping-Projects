import requests 
import pandas as pd 
import time
import random
import sqlite3
from hs_code_scraper import next_page_link,page_scraper
from urllib import parse
import brotli
import datetime
from bs4 import BeautifulSoup
import json
import os

form_data = {'type': 'export', 'searchkey': '8422', 'company_id': '', 'core': 'exports', 'from_date': '01/01/2016', 'to_date': '09/30/2019', 'unfiltered_data': '0'}

#displays error
def display_error(error):
	print(error)

#changes seconds to desired time format
def time_converter(x):
    x = int(x)
    if (x//60)==0:
        return str(x)+' sec'
    elif(x//3600==0):
        return str(x//60)+' min '+str(x%60)+' sec'
    elif(x//(3600*24)==0):
        return str(x//3600) +' hrs ' + str((x%3600)//60)+' min '+str((x%3600)%60)+' sec'
    else:
        return str(x//(24*3600))+' days '+ str((x%(24*3600))//3600)+' hrs '+ str(((x%(24*3600))%3600)//60)+' min '+str(((x%(24*3600))%3600)%60)+' sec'

#tries to connect with the server
def download_it(url,num_tries = 1):
	try:
		r = requests.post(url,data = form_data ,headers = headers)
		return ('OK',r)
	except Exception as e:
		if(num_tries<=5):
			time.sleep(2*num_tries)
			return download_it(url,num_tries+1)
		else:
			display_error(f'some network connection problem is occuring again and again due to:-\nError: {str(e)}\nType of Error : {str(type(e))}')
			return('ERROR',None)

def join(cookie_dict):
    cookie = ''
    for i in cookie_dict:
        t = i+'='+cookie_dict[i]+'; '
        cookie+=t
    return cookie[:-2]

#for fetching headers with cookies from firefox browser
def fetch_headers():
    conn = sqlite3.connect(r'C:\Users\ADITYA JAIN\AppData\Roaming\Mozilla\Firefox\Profiles\0ndwurz0.default\cookies.sqlite')
    c = conn.cursor()
    c.execute('SELECT name,value FROM moz_cookies where baseDomain = "thedollarbusiness.com"')
    data = c.fetchall()
    cookie_dict = {}
    for i in data:
        cookie_dict[i[0]]=i[1]
    try:
    	del cookie_dict['exim_data_analysis']
    except:
    	pass
    headers = {'Host': 'www.thedollarbusiness.com',
               'Connection': 'keep-alive',
               'Content-Length': '121',
               'Accept': '*/*',
               'Origin': 'https://www.thedollarbusiness.com',
               'x-Requested-With': 'XMLHttpRequest',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36',
               'Sec-Fetch-Mode': 'cors',
               'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
               'Sec-Fetch-Site': 'same-origin',
               'Referer': 'https://www.thedollarbusiness.com/export-'+form_data['searchkey']+'-hs-code?query='+form_data['searchkey']+'&type=export&from_date='+form_data['from_date']+'&to_date='+form_data['to_date'],
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.9',
               'cookie': parse.unquote(join(cookie_dict))}
    return headers
headers = fetch_headers()

#making necessary folders
if(not os.path.isdir('HS_CODE_DATA')):
    os.mkdir('HS_CODE_DATA')
if(not os.path.isdir('time_analysis')):
	os.mkdir('time_analysis')

#defining name of hs code file
file_name = 'HS_CODE_DATA\\'+'hs-code-'+form_data['searchkey']+'.csv'

#intializing some data
cols = ['Page No','link','Date','Shipment Id','HS Code','Product description','Buyer country','Buyer','Destination Port','Seller country','Seller','Origin Port','Unit','Quantity','Value(USD)','Unit price']
first_page_url ='''https://www.thedollarbusiness.com/exim/exim_data/get_company_shipments/cG5CODVuODBuOW1NNm54TWZCY21Odz09/U3lacFJFU3Z1QVBQd3NhRmZjL3dJNndISjRJQm1rR29nS2EvamVWcS9sZk1WZlY5VVlydWhueDExTzBlcEJObg=='''
    
#handles the contnuing of the crawler from where it was stopped
def continuer(file_name):
	if(not os.path.isfile(file_name)):
		start = pd.DataFrame(columns=cols)
		start.to_csv(file_name,index = False)
		return ('OK',0,first_page_url)
	else:
		data = pd.read_csv(file_name,lineterminator = '\n')
		if(data.shape[0]==0):
			return ('OK',0,first_page_url)
		page_no = int(data.iloc[-1]['Page No'])
		link = data.iloc[-1]['link']

		(status,r) = download_it(link)
		if(status=='ERROR'):
			return ('ERROR',None,None)
		try:
			html = r.content
			html = brotli.decompress(html)
			soup = BeautifulSoup(html,'html.parser')
			(next_page_url,comment) = next_page_link(soup)
			if(next_page_url==None):
			    open('why.txt','wb').write(b'ERROR in next_page_link\n'+html)
			    display_error(f'ERROR at starting from page no = {page_no+1}\nReason : {comment}')
			    return ('ERROR',None,None)
			else:
				page_url = next_page_url
				print(f'Success at starting from page no = {page_no+1}')
				return ('OK',page_no,page_url)
		except Exception as e:
			display_error(f'{e} at starting from page no = {page_no+1}')
			return('ERROR',None,None)

(status,page_no,page_url) = continuer(file_name)
if(status=='OK'):
	pass
else:
	exit()

t_anlsys = {}
start_page_no = page_no
start_time = time.time()
print(f'started at {datetime.datetime.now()} with page no. = {page_no+1}')

#processs starts for the current page url
while True:
    page_process_start = time.time()
    time.sleep(random.randint(1,10)/10)
    page_no+=1
    request_start = time.time()
    (status,r) = download_it(page_url)
    request_end = time.time()
    if(status=='OK'):
    	pass
    else:
    	break
    html = r.content
    html = brotli.decompress(html)
    if(r.status_code!=200):
        print(f'there is some error in connecting to site due to Status_code : {r.status_code}')
        break
    else:
        try:
            soup = BeautifulSoup(html,'html.parser')
            cookie_pass = soup.find('li',{'class':'active'})==None
        except Exception as e:
            display_error(f'type of error : {type(e)}\nError : {e}\noccurred')
            break
        if(cookie_pass):
            display_error('cookie failure : please reset the cookie')
            break
        else:
            scrap_start = time.time()
            Info = page_scraper(soup)
            scrap_end = time.time()
            if(not Info):
                pass
            else:
                l = len(Info['Date'])
                Info['Page No']=[str(page_no)]*l
                Info['link']=[page_url]*l
                final = pd.DataFrame(Info,columns=cols)
                append_start = time.time()
                final.to_csv(file_name,mode='a',index = False,header=False)
                append_end = time.time()
                print(f'{page_no} completed')

            (next_page_url,comment) = next_page_link(soup)
            if(next_page_url==None):
                print(f'process Eneded at page No. -- {page_no}\nReason : {comment}')
                break
            page_url = next_page_url
    page_process_end = time.time()
    t_anlsys['page_no']=page_no
    t_anlsys['scrap_time']=scrap_end - scrap_start
    t_anlsys['append_time']=append_end - append_start
    t_anlsys['request_time']=request_end - request_start
    t_anlsys['page_process_time']=page_process_end - page_process_start
    open('time_analysis\\time_analysis_json_'+form_data['searchkey']+'.txt','a').write(json.dumps(t_anlsys)+'\n')

print(f'ended at {datetime.datetime.now()}')
end_page_no = page_no
end_time = time.time()
time_gap = end_time-start_time
page_gap = end_page_no-start_page_no
print(f'total time taken = {time_converter(time_gap)} at an average of {time_gap/page_gap} secs per page')
