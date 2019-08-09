# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 11:52:07 2019

@author: uday.gupta
"""
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from newspaper import Article
from datetime import date
from dateutil.parser import parse
from tqdm import tqdm

driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
driver.get("https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin")

mail_path = driver.find_element_by_xpath('//*[@id="identifierId"]')
mail_path.send_keys("standardbk.alerts@gmail.com")
driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
time.sleep(5)
wait = WebDriverWait(driver, 20)
try:
#    mail_pass = driver.find_element_by_xpath('//*[@id="password"]/div[1]/div/div[1]/input')

    password = wait.until(EC.element_to_be_clickable((By.NAME,'password'))).send_keys("passwd@123")
#    mail_pass.send_keys("passwd@123")
    driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
    time.sleep(5)
except:
    print("Error in password loading")

#html = driver.page_source
#soup = BeautifulSoup(html)
##print(soup)
#
#table=soup.find("table", { "class":"F cf zt"})
##print(table)
##table = soup.find('table',{ "id":":2u"})
#
##print(row[0])
#
#row=table.findChildren(['tr'])


import pandas as pd
Top=['Received time','Subject','Url','Title','News_Text']
table_data=pd.DataFrame()# we create a empty dataframe
table_data=pd.DataFrame(columns=Top)
Stop_val=True
l=0
try:
    while Stop_val==True and l<=1:
        html = driver.page_source
        soup = BeautifulSoup(html,features="lxml")
        #print(soup)

        table=soup.find("table", { "class":"F cf zt"})
        #print(table)
        #table = soup.find('table',{ "id":":2u"})

        #print(row[0])

        row=table.findChildren(['tr'])
        for i in row:
            t=[]
            text_body=[]
            for j in str(i).split():
                t.append(j)
            xpath='//*[@'+t[5]+']'
            mail_title =wait.until(EC.presence_of_element_located((By.XPATH,xpath)))
            mail_data=[]
            for j in mail_title.text.split("\n"):
                mail_data.append(j)
            if mail_data[0]=='Google Alerts':
                subject=mail_data[1]
                date1=mail_data[len(mail_data)-1]
                val=parse(str(date1))
            mail_title.click()
            time.sleep(5)
            html_news=driver.page_source
            soup1=BeautifulSoup(html_news,'html.parser')
            table1=soup1.find("table", { "class":"Bs nH iY bAt"})
            row1=table1.findChildren(['tr'])
            urls=[]
            for i in str(row1).split(" "):
                #print(i)
                url=''
                atri= None
                text_body=[]
                try:
                    result = str(i).index('url=https:www.//')
                    b=str(i)
                    for i in range(result+4,result+200):
                        if b[i] =='&':
                            break
                        else:
                            url=url+b[i]
                    if url not in urls:
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
                                table_data = table_data.append({'Received time':val.strftime(" %d-%m-%Y ,%I:%M%p"),'Subject':subject,'Url':url,'Title':atri,'Text_body':text_val},ignore_index=True,sort=False)
                except:
                    try:
                        result = str(i).index('url=https://')
                        b=str(i)
                        for i in range(result+4,result+200):
                            if b[i] =='&':
                                break
                            else:
                                url=url+b[i]
                        if url not in urls:
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
                                table_data = table_data.append({'Received time':val.strftime(" %d-%m-%Y ,%I:%M%p"),'Subject':subject,'Url':url,'Title':atri,'Text_body':text_val},ignore_index=True,sort=False)
                        continue
                    continue
            print(table_data.shape)
            wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id=":4"]/div[2]/div[1]/div/div[1]/div/div'))).click()
            time.sleep(3)
        driver.find_element_by_xpath('//*[@id=":13e"]').click()
        time.sleep(5)
        l=l+1
        #table_data.to_csv("E:/googleAlert/res/googleAlert.csv")
except:
    Stop_val=False
table_data.to_csv("E:/googleAlert/res/googleAlert.csv")
