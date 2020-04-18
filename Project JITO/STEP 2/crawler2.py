#crawler for getting details of jito members by crawling one by one over profile links from links.csv

#importing necessary libraries
import requests 
import pandas as pd
import time
import datetime
import json
import os
import sqlite3
from bs4 import BeautifulSoup
from scraper2 import page_scraper

#for converting time
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

#for printing errors (some gui can be addded later on)
def display_error(error):
    print(error)

#defining some variables
column_names  = ['index','profile link','name of person','chapter name','user type','basic information','contact information','company details','education & work experience','family details']
path_to_headers = '..\\DATA\\UTILS\\headers.json'
file_path_to_links = '..\\DATA\\PROFILE LINKS\\links.csv'
records_file_path = '..\\DATA\\MEMBER DETAILS\\'

#intializing headers
HEADERS = json.loads(open(path_to_headers,'r').read())

#for getting cookies
def get_cookies():
    conn = sqlite3.connect(r'C:\Users\chatu\AppData\Roaming\Mozilla\Firefox\Profiles\g966pl3l.default\cookies.sqlite')
    c = conn.cursor()
    c.execute('SELECT name,value FROM moz_cookies where baseDomain = "jito.org"')
    entries = c.fetchall()
    cookie_dict = {}
    for entry in entries:
        cookie_dict[entry[0]]=entry[1]
    return cookie_dict

COOKIES = get_cookies()


#creating list of exhibition links
data = pd.read_csv(file_path_to_links)
links = list(data['profile link'])

#very important if running the script on multiple systems by dividing the work
MIN_INDEX = 0
MAX_INDEX = 6000#len(links)

#for getting url
def get_url(index):
    return links[index]

#returns r.content for url if response status code is 200
def downloader(url,tries = 0):
    global COOKIES
    try:
        r = requests.get(url,headers = HEADERS,cookies = COOKIES,timeout = 60)
        if(r.status_code==200):
            return ('Success',r.content)
        elif(500 <= r.status_code < 600):
            if(tries < 3):
                time.sleep(5*(tries+1))
                return downloader(url,tries+1)
            else:
                error_message = f'internal server error at url = {url}'
                return (error_message,str.encode(error_message)+b'\n\n\n'+r.content)
        else:
            error_message = f'Technical failure due to status_code = {r.status_code} at url = {url}'
            return (error_message,str.encode(error_message)+b'\n\n\n'+r.content)
    except Exception as e:
        if(tries < 3):
            time.sleep(5*(tries+1))
            print(f'ERROR_TYPE = {type(e)}\nERROR : {e}\nAt try no : {tries} at url : {url}\n')
            return downloader(url,tries+1)
        else:
            return ('see above 3 ERRORs for reference',str.encode(f'No r.content avaialble as downloader went in except command 3 times at url = {url}'))

#for continuing from where it was last stopped
def continuer():
    if(not os.path.isfile(records_file_path+'records.csv')):
       pd.DataFrame(columns=column_names).to_csv(records_file_path+'records.csv',index = False)
       return MIN_INDEX
    data = pd.read_csv(records_file_path+'records.csv')
    if data.empty:
       return MIN_INDEX
    return int(data.iloc[-1]['index'])+1

def continuer1():
    if(not os.path.isfile(records_file_path+'last_record_no_crawled.txt')):
       pd.DataFrame(columns=column_names).to_csv(records_file_path+'records.csv',index = False)
       return MIN_INDEX
    last_index = open(records_file_path+'last_record_no_crawled.txt','r').read()
    return int(last_index)+1

#initializing index from continuer
index = continuer()

print('-'*60)
print(f'started at {datetime.datetime.now()} with record no. = {index}')
print('-'*60)
start_time = time.time()

#crawling started
while True:
    (status,html) = downloader(get_url(index))
    if(status=='Success'):
        soup = BeautifulSoup(html,'html.parser')
        if(soup.find('title').text.lower()=='Login'.lower()):
            display_error('Cookies Reset Needed.......PLEASE go to JITO Website....SIGN IN and Then restart CRAWLER2')
            break

        Info = page_scraper(soup)

        Info['index'] = str(index)
        Info['profile link'] = links[index]

        df = pd.DataFrame(Info,columns = column_names,index = [1])
        df.to_csv(records_file_path+'records.csv',mode='a',header = False,index = False)
        open(records_file_path+'last_record_no_crawled.txt','w').write(str(index))
        print(f'record no. = {index} completed')
        index+=1
    else:
        display_error(status)
        open(records_file_path+'errors.txt','wb').write(html)
        break

    if(index==MAX_INDEX):
        print('*'*80)
        print(f'Process of fetching Records Completed at RECORD NO. = {index-1}')
        print('Please confirm it manually by seeing the no. of records in links.csv')
        print('*'*80)
        break

end_time = time.time()
print('-'*60)
print(f'ended at {datetime.datetime.now()} with record no. = {index}')
print(f'Total time taken : {time_converter(end_time-start_time)}')
print('-'*60)


