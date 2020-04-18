#crawler for getting links of various exhibitions by crawling over pages like 1,2,3... and so on 

#importing necessary libraries
import requests 
import pandas as pd
import time
import datetime
import json
import os
from scraper1 import page_scraper

#for printing errors (some gui can be addded later on)
def display_error(error):
    print(error)

#defining some variables
main_page_url = 'https://www.expocheck.com/en/expo#'
column_names  = ['pageindex','expo_link','past_date_and_location']
path_to_headers = '..\\DATA\\UTILS\\headers.json'
file_path = '..\\DATA\\EXHIBITION LINKS\\CURRENT VERSION\\'

#intializing headers
HEADERS = json.loads(open(path_to_headers,'r').read())

#for getting cookies
def get_cookies():
    r = requests.get(main_page_url,headers=HEADERS)
    return r.cookies
COOKIES = get_cookies()

#for getting url of pageindex = index
def get_url(index):
    return f'https://www.expocheck.com/en/expo/expopaging?pageindex={index}'

#returns r.content for url if response status code is 200
def downloader(url,tries = 0):
    global COOKIES
    try:
        r = requests.get(url,headers = HEADERS,cookies = COOKIES,timeout = (30,60))
        if(r.status_code==200):
            return ('Success',r.content)
        elif(r.staus_code==500):
            COOKIES = get_cookies()
            if(tries < 3):
                return downloader(url,tries+1)
            else:
                error_message = f'Cookie change not working at url = {url}'
                return (error_message,str.encode(error_message)+b'\n\n\n'+r.content)
        else:
            error_message = f'Technical failure due to satus_code = {r.status_code} at url = {url}'
            return (error_message,str.encode(error_message)+b'\n\n\n'+r.content)
    except Exception as e:
        if(tries < 3):
            time.sleep(5*(tries+1))
            print(f'ERROR_TYPE = {type(e)}\nERROR : {e}\nAt try no : {tries} at url : {url}\n')
            return downloader(url,tries+1)
        else:
            return ('see above 5 ERRORs for reference',str.encode(f'No r.content avaialble as downloader went in except command 5 times at url = {url}'))

#for continuing from where it was last stopped
def continuer():
    if(not os.path.isfile(file_path+'links.csv')):
       pd.DataFrame(columns=column_names).to_csv(file_path+'links.csv',index = False)
       return 1
    data = pd.read_csv(file_path+'links.csv')
    if data.empty:
       return 1
    return int(data.iloc[-1]['pageindex'])+1

def continuer1():
    if(not os.path.isfile(file_path+'last_pageindex_crawled.txt')):
       pd.DataFrame(columns=column_names).to_csv(file_path+'links.csv',index = False)
       return 1
    last_index = open(file_path+'last_pageindex_crawled.txt','r').read()
    return int(last_index)+1

#getting index from continuer
index = continuer()

print('-'*60)
print(f'started at {datetime.datetime.now()} with pageindex = {index}')
print('-'*60)
start_time = time.time()

#crawling started
while True:
    (status,html) = downloader(get_url(index))
    if(status=='Success'):
        Info = page_scraper(html)
        if(not Info):
            print('*'*80)
            print(f'Process of Finding Links Completed at Pageindex = {index}')
            print('Please confirm it manually by going on last page of Expocheck website')
            print('*'*80)
            break
        else:
            Info['pageindex'] = len(Info['expo_link'])*[index]
            df = pd.DataFrame(Info,columns = column_names)
            df.to_csv(file_path+'links.csv',mode='a',header = False,index = False)
            open(file_path+'last_pageindex_crawled.txt','w').write(str(index))
            print(f'pageindex = {index} completed')
            index+=1
    else:
        display_error(status)
        open(file_path+'errors.txt','wb').write(html)
        break

end_time = time.time()
print('-'*60)
print(f'ended at {datetime.datetime.now()} with pageindex = {index}')
print(f'Total time taken : {time_converter(end_time-start_time)}')
print('-'*60)


