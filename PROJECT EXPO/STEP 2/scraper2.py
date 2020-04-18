from bs4 import BeautifulSoup

def clear_it(value):
    return value.strip('\n').strip(' ').strip('\r').strip('\n').strip(' ').strip('\r')

#function for extracting general information
def General_Info(soup,Info):
    cols = ['exhibition name','exhibition description','future date','location','first year of expo','show type','branches','frequency','expo website','open to']
    for i in cols:
        Info[i]='NA'

    #for extracting exhibition name
    name = soup.find('h1',{'class':'expo-h1'})
    if(name!=None):
        Info['exhibition name'] = clear_it(name.text).split('\r\n')[0]

    #for extracting exhibition description
    desc=name.find('span')
    if(desc!=None):
        Info['exhibition description'] = desc.text

    #for extracting location
    overview = soup.find('div',{'id':'Overview'})
    if(overview!=None):
        media_pt3=overview.find_all('div',{'class':'media pt-3'})
        for media in media_pt3:
            if(media!=None):
                if(media.find('strong')!=None and ('Location' in media.find('strong').text)):
                    Info['location'] = media.text.split('Location')[-1]

    #for extracting future date
    if(overview!=None):
        date=overview.find('h5')
        if(date!=None):
            Info['future date'] = date.text
            if(len(date.text.split())==0):
                Info['future_date']='NA'
    
    #for fetching more facts
    facts = ['first year of expo','show type','branches','frequency','expo website','open to']
    temp = {}
    more_facts = soup.find('table',{'class':'mytable'})
    if more_facts!=None:
        rows = more_facts.find_all('tr')
        for row in rows:
            if(row!=None):
                cols = row.find_all('td')
                if(len(cols)>1):
                    temp[cols[0].text.lower()] = cols[1].text
    for i in temp:
        if i in facts:
            Info[i]=temp[i]

#function for extracting expo statistics json
def Expo_Statistics(soup,Info):
    temp = {'total':'NA','foreign':'NA','national':'NA'}

    years=[]
    options = soup.find_all('option')
    for option in options:
        try:
            years.append(option['data-option-year'])
        except:
            pass
    list(dict.fromkeys(years))

    body=soup.find('div',{'class':'structured-box-body'})
    main_dict = {}
    for year in years:
        entries = body.find_all('div',{'data-year':year})
        dd = {'net sqm' : temp ,'exhibitors' :temp,'visitors': temp}
        for entry in entries:
            d = temp
            heading = entry.find('h4')
            if(heading!=None):
                heading =clear_it(heading.text).lower()
                total = entry.find('h2')
                if(total!=None):
                    d ['total'] = total.text.strip()
                pp = entry.find_all('p')
                if(len(pp)!=0):
                    for i in range(min(len(pp),2)):
                        t = pp[i].text.split(':')
                        d[t[0].lower().strip()] = t[-1].lower().strip()
                dd[heading] = d
        main_dict[year] = dd
    Info['expo statistics'] = json.dumps(main_dict)


#function for extracting orgnaiser information json
def Organiser_Info(soup,Info):
    main_dict = {}
    names=soup.find_all('div',{'class':'mt-4 mb-4'})
    for name in names:
        if(name!=None):
            if(name.find('h4',{'class':'toUpper'})!=None):
                if(name.find('h4',{'class':'toUpper'}).text=='EVENT ORGANISER'):
                    p = name.find('p',{'class':'toUpper'})
                    if(p!=None):
                        org_name = p.text
                        add=''
                        for tag in name.find('p').next_siblings:
                            if tag.name=='p':
                                d = {}
                                clean=BeautifulSoup(add,'html.parser')
                                d['organiser address'] = clean.text.split('Open Website')[0]
                                try:
                                    d['organiser website'] = clean.find('a')['href']
                                except:
                                    d['organiser website'] = 'NA'
                                main_dict[org_name]=d
                                add=''
                                org_name = tag.text
                                continue
                            else:
                                add+=str(tag)
                        d = {}
                        clean=BeautifulSoup(add,'html.parser')
                        d['organiser address'] = clean.text.split('Open Website')[0]
                        try:
                            d['organiser website'] = clean.find('a')['href']
                        except:
                            d['organiser website'] = 'NA'
                        main_dict[org_name]=d
    Info['organiser data']=json.dumps(main_dict)

def page_scraper(html):
    Info = {}
    soup = BeautifulSoup(html,'html.parser')
    General_Info(soup,Info)
    Expo_Statistics(soup,Info)
    Organiser_Info(soup,Info)
    return Info

