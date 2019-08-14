# -*- coding: utf-8 -*-
"""
Created on Mon Aug 12 12:45:52 2019

@author: uday.gupta
"""

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from newspaper import Article
import newspaper
from datetime import date
import schedule
def job():
    driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
    # we are giving the url of the gamil.com
    driver.get("https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
    # we are sending the gmail id
    mail_path = driver.find_element_by_xpath('//*[@id="identifierId"]')
    mail_path.send_keys("standardbk.alerts@gmail.com")
    driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
    time.sleep(2)
    wait = WebDriverWait(driver, 20)
    # we are sending the password
    try:
        password = wait.until(EC.element_to_be_clickable((By.NAME,'password'))).send_keys("passwd@123")
        driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
        time.sleep(5)
    except:
        print("Error in password loading")

    #table declearation
    import pandas as pd
    Top=['Received time','Keyword','Subject','Url','Title','Text_body']
    table_data=pd.DataFrame()# we create a empty dataframe
    table_data=pd.DataFrame(columns=Top)
    # we are providing the xpath of the each mail so that we can click on each mail and get the data from each mail on that days
    table_id1=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id=":2v"]'))).click()
    # get the source code of the page
    html_news=driver.page_source
    # parse the code  using beautifulsoup
    soup1=BeautifulSoup(html_news,'html.parser')
    #soup1
    # find a specific class using class name from the table
    table1=soup1.find("table", { "class":"Bs nH iY bAt"})
    #table1
    # finding each row of the table
    row1=table1.findChildren(['tr'])
    #print(row1[0])
    import re
    dt=str(row1[0])
    #split the each element by space
    da=[x for x in dt.split(' ')]
    #print(da)
    key_val=[]
    # these are the text that i need to find so that i can get the right keyword,Urls from the page source
    b=['style="color:#262626;font-size:22px">"','url=https:www.//','url=https://']
    urls=[]
    for i in range(len(da)):
        url=''
        try:
            m=str(da[i]).index(b[0])
            #print(i)
            #print(da[i])
            #i=1395
            key=''
            for k in range(i,i+6):
                #print(da[k])
                st=str(da[k])
                if i!=k:
                    if st !='style="padding-left:32px"></td>':
                        for p in range(len(st)):
        #                    p = 6
                            if st[p] =='<' or st[p] ==' ' or st[p] =='\n' :
                                break
                            else:
                                key=key+st[p]
                        key=key+" "
                else:
                        for p in range(37,len(st)):
                            key=key+st[p]
                        key=key+" "
            print(key)
            key_val.append(key)
        except:
            try:
                #print('2')
                m=str(da[i]).index(b[2])
                #print(i)
                for j in range(m+4,m+200):
                    if str(da[i])[j] =='&':
                        break
                    else:
                        url=url+str(da[i])[j]
                #print(url)
                if url not in urls:
                    urls.append(url)
                    #print("all the Urls:", urls)
                    article = Article(url)
                    article.download()
                    Articles=BeautifulSoup(article.html,'html.parser')
                    arti=Articles.title.string
                    if arti != None:
                        sina_paper = newspaper.build(url,language='en')
                        article = sina_paper.articles[1]
                        article.download()
                        article.parse()
                        text_val= article.text
                        table_data = table_data.append({'Received time':' 08-08-2019 ,08:00AM','Keyword':key,'Subject':'Google Alert â€“ Daily Digest','Url':url,'Title':arti,'Text_body':text_val},ignore_index=True,sort=False)
                        #print(table_data)
            except:
                try:
                    #print('3')
                    m=str(da[i]).index(b[1])
                    #print(i)
                    for j in range(m+4,m+200):
                        if str(da[i])[j] =='&':
                            break
                        else:
                            url=url+str(da[i])[j]
                    #print(url)
                    if url not in urls:
                        urls.append(url)
                        #print("all the Urls:", urls)
                        article = Article(url)
                        article.download()
                        Articles=BeautifulSoup(article.html,'html.parser')
                        arti=Articles.title.string
                        if arti != None:
                            sina_paper = newspaper.build(url,language='en')
                            article = sina_paper.articles[1]
                            article.download()
                            article.parse()
                            text_val= article.text
                            table_data = table_data.append({'Received time':' 08-08-2019 ,08:00AM','Keyword':key,'Subject':'Google Alert â€“ Daily Digest','Url':url,'Title':arti,'Text_body':text_val},ignore_index=True,sort=False)
                            #print(table_data)
                except:
                    continue
                continue
            continue
    print(table_data)
    table_data.to_csv("E:/googleAlert/res/googleAlerts_sample1.csv")

schedule.every().days.at("11:30").do(job())
