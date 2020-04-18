import json
import numpy as np

def clear_it(value):
    bad_chars = ['\t','\r','\n']
    for i in bad_chars:
        value = value.replace(i,' ')
    return value.strip(' ')


def page_scraper(soup):
    cols=['name of person','chapter name','user type','basic information','contact information','company details','education & work experience','family details']
    Info = {}
    for i in cols[:3]:
        Info[i] = np.nan
    for i in cols[3:]:
        Info[i] = json.dumps({})

    #some basic details
    Profile_name = soup.find('div',{'class':'welcometext'})
    if(Profile_name!=None):
        Info['name of person'] = clear_it(Profile_name.text)
    chap_name = soup.find('div',{'class':'chap_name'})
    if(chap_name!=None):
        Info['chapter name']= clear_it(chap_name.text)
    user_type = soup.find('div',{'class':'user_type'})
    if(user_type!=None):
        Info['user type']= clear_it(user_type.text)

    #rest others
    others = soup.findAll('div',{'class':'cProfile-About'})
    for other in others:
        details = {}
        heading = other.find('h4')
        if(heading!=None):
            datas = other.findAll('div',{'class':'data'})
            for data in datas:
                try:
                    dt = data.find('dt').text
                    dt = clear_it(dt).lower()
                except:
                    continue
                try:
                    dd = data.find('dd').text
                    dd = clear_it(dd).lower()
                except:
                    continue
                details[dt]=dd
            Info[clear_it(heading.text).lower()]= json.dumps(details)

    
    #company details
    company = soup.find('div',{'class':'companyinfo cProfile-About'})
    if(company!=None):
        details = {}
        datas = company.findAll('div',{'class':'data'})
        for data in datas:
            try:
                dt = data.find('dt').text
                dt = clear_it(dt).lower()
            except:
                continue
            try:
                dd = data.find('dd').text
                dd = clear_it(dd).lower()
            except:
                continue
            try:
                aaa = details[dt]
            except:
                details[dt]=dd
        Info['company details'] = json.dumps(details)
    
    #family details
    family = soup.find('div',{'class':'familyinfo cProfile-About'})
    if(family!=None):
        details = {}
        mapper = {}
        rows = family.findAll('div',{'class':'rowdata'})
        for row in rows:
            datahead = row.find('div',{'class':'data head'})
            if(datahead!=None):
                relation = datahead.text.lower()
                if(not relation.split()):
                    continue
                try:
                    mapper[relation] = mapper[relation]+1
                except:
                    mapper[relation] = 1
                d = {}
                datas = row.findAll('div',{'class':'data'})
                for data in datas:
                    try:
                        dt = data.find('dt').text
                        dt = clear_it(dt).lower()
                    except:
                        continue
                    try:
                        dd = data.find('dd').text
                        dd = clear_it(dd).lower()
                    except:
                        continue
                    d[dt]=dd
                details[clear_it(relation)+'_'+str(mapper[relation])] = d
        Info['family details'] = json.dumps(details)

    
    Res = {}
    for i in Info:
        if i in cols:
            Res[i] = Info[i]
    return Res
