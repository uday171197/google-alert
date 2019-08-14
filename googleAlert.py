# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 11:52:07 2019

@author: uday.gupta
"""
#these are teh library for the scaping the data from gmail
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from newspaper import Article
import newspaper
from datetime import date
from dateutil.parser import parse
import logging
#these are the lobrary for the sending the mail Daily
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import datetime
import os
import sys

def Daily_Mail():
    """
    Daily_Mail():

    This function is written to  send the Google alert data from aratoengbot@gmail.com to respected  recipients by mail  and at the end it will show whether the mail is send or not  .

    This function will call by job function after creating the dataset of google alert

    """

    sender = 'aratoengbot@gmail.com'
    gmail_password = 'dpa@1234'
    recipients = ['tejal.joshi@decimalpointanalytics.com>', 'neha.beerwala@decimalpointanalytics.com', ' sonali.phadol@decimalpointanalytics.com','uday.gupta@decimalpointanalytics.com']
    COMMASPACE = ', '
    # Create the enclosing (outer) message
    outer = MIMEMultipart()
    outer['Subject'] = 'Google Alert daily news data set report Extracted at {}'.format(str(datetime.datetime.utcnow())[:10])
    outer['To'] = COMMASPACE.join(recipients)
    outer['From'] = 'Google Alerts'
    outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'



    # List of attachment
    os.chdir("E:/googleAlert/res")
    intresting_files = os.listdir("E:/googleAlert/res")
    # Add the attachments to the message
    for file in intresting_files:
        try:
            with open(file, 'rb') as fp:
                msg = MIMEBase('application', "octet-stream")
                msg.set_payload(fp.read())
            encoders.encode_base64(msg)
            msg.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file))
            outer.attach(msg)

        except:
            logging.error("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            print("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
            raise



    composed = outer.as_string()



    # Send the email
    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as s:
            s.ehlo()
            s.starttls()
            s.ehlo()
            """It is going to login by the given id and password"""
            s.login(sender, gmail_password)
            s.sendmail(sender, recipients, composed)
            s.close()
        print("Email sent!")
        logging.info("Email sent!")
    except:
        logging.error("Unable to open one of the attachments. Error: ", sys.exc_info()[0])
        print("Unable to send the email. Error: ", sys.exc_info()[0])
        raise

# I define a function job  that that scaap the  data from gmail
def Job():
    """
    def Job():

This is the code for scraping the data from the mail that are provided by the standard bank. Basictly It is written for the daily based so that
we we can scrap the data daily and send it to recipients.Firts it will check google Alert mail date and today date are same then it will open the mail and fid all the Keywords ,article links . then I pass that link to article  maodule that give the title of the article and also pass to newspaper module that give the text body of that mail. I will put every value into dataframe and then convert the DataFrameinto excel sheet.

    """
    logging.basicConfig(filename='app.log', filemode='w', format='%(name)s - %(levelname)s - %(message)s')
    logging.warning('This will get logged to a file')
    T=True
    while T==True:
        try:
            driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
            # we are giving the url of the gamil.com
            driver.get("https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
            # we are sending the gmail id
            mail_path = driver.find_element_by_xpath('//*[@id="identifierId"]')
            mail_path.send_keys("standardbk.alerts@gmail.com")
            driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
            #time.sleep(2)
            wait = WebDriverWait(driver, 20)
            # we are sending the password
            try:
                password = wait.until(EC.element_to_be_clickable((By.NAME,'password'))).send_keys("passwd@123")
                driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
                time.sleep(5)
            except:
                logging.error("Error in password loading")
                print("Error in password loading")

            #table declearation
            import pandas as pd
            Top=['Received time','Keyword','Subject','Url','Title','Text_body']
            table_data=pd.DataFrame()# we create a empty dataframe
            table_data=pd.DataFrame(columns=Top)

            html = driver.page_source
            soup = BeautifulSoup(html,features="lxml")
            #print(soup)

            table=soup.find("table", { "class":"F cf zt"})
            #print(table)
            #table = soup.find('table',{ "id":":2u"})

            #print(row[0])
        #finding all the child of the table
            row=table.findChildren(['tr'])
            i=row[0]
            t=[]
            text_body=[]
            #this for loop find the id of each mail in the gmail
            for j in str(i).split():
                t.append(j)
            #it generate the xpath Automaticaly
            xpath='//*[@'+t[5]+']'
            #finding the element at that xpath
            mail_title =wait.until(EC.presence_of_element_located((By.XPATH,xpath)))
            mail_data=[]
            for j in mail_title.text.split("\n"):
                mail_data.append(j)
            #it check whether the mail is of  google alert is or not
            if mail_data[0]=='Google Alerts':
                #finding the sublect of the mail
                subject=mail_data[1]
                date=mail_data[len(mail_data)-1]
                val=parse(str(date))
                print(val.strftime(" %d-%m-%Y ,%I:%M%p"))
                #Finding the mail date with to_time
                value1_of_mail=val.strftime(" %d-%m-%Y")
                #print(value1_of_mail)
            #finding the todays date
            from datetime import date
            today_date = date.today()
            todaydate=parse(str(today_date))
            value1_of_today=todaydate.strftime(" %d-%m-%Y")
            #print(value1_of_today)
            #this is the code to find all the mail of the same date
            logging.info('Google Alert daily news data set report Extracted at {}'.format(str(val.strftime(" %d-%m-%Y ,%I:%M%p"))))
            if value1_of_mail == value1_of_today :
                #clicking on the first mail
                mail_title.click()
                time.sleep(2)
                html_news=driver.page_source
                soup1=BeautifulSoup(html_news,'html.parser')
                table1=soup1.find("table", { "class":"Bs nH iY bAt"})
                row1=table1.findChildren(['tr'])
                import re
                dt=str(row1[0])
                #split the each element by space
                da=[x for x in dt.split(' ')]
                #print(da)
                key_val=[]
            # these are t
                #print(i)
                url=''
                atri= None
                text_body=[]
                #these are the substring that i am searching in the code so that i can find the Keyword or news article link
                b=['style="color:#262626;font-size:22px">"','url=https:www.//','url=https://']
                urls=[]
                #print(len(da))
                for i in range(len(da)):
                    url=''
                    try:
                        #this is for to find the Keyword fron the mail
                        m=str(da[i]).index(b[0])
                        #print(i)
                        #print(da[4615])
                        #i=4422
                        key=' '
                        for k in range(i,i+5):
                            st=str(da[k])
                            #print(st)
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
                        #print(key)
                    except:
                        try:# this is to find the ulr of the mail which is start with ,'url=https:www.//'
                            #print('2')
                            m=str(da[i]).index(b[2])
                            #print(i)
                            #It generate a url by adding word by word
                            for j in range(m+4,m+200):
                                if str(da[i])[j] =='&':
                                    break
                                else:
                                    url=url+str(da[i])[j]
                            #print(url)
                            # this if loop is use to remove the dupliction of the mail
                            if url not in urls:
                                urls.append(url)
                                #this code is for to find the title of the articles
                                article = Article(url)
                                article.download()
                                Articles=BeautifulSoup(article.html,'html.parser')
                                arti=Articles.title.string

                                if arti != None:
                                    #print("Article:",arti)
                                    # this code for finding the text body of the that url of the mail
                                    article = Article(url)
                                    article.download()
                                    article.parse()
                                    # training_set_file['authors'][i]= article.authors
                                    text_val= article.text
                                    #print("text_body:", text_val)
                                    # putting the each value into the DataFrame
                                    table_data = table_data.append({'Received time':val.strftime(" %d-%m-%Y"),'Keyword':key,'Subject':subject,'Url':url,'Title':arti,'Text_body':text_val},ignore_index=True,sort=False)
                                    logging.info(subject)
                                    #print("all the Urls:", urls)
                                    #print(table_data)

                        except:
                            try:
                                # this is to find the ulr of the mail which is start with ,'url=https://'
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
                                    article = Article(url)
                                    article.download()
                                    Articles=BeautifulSoup(article.html,'html.parser')
                                    arti=Articles.title.string
                                    if arti != None:
                                        #print("Article:",arti)
                                        article = Article(url)
                                        article.download()
                                        article.parse()
                                        # training_set_file['authors'][i]= article.authors
                                        text_val= article.text
                                        #print("text_body:" ,text_val)
                                        table_data = table_data.append({'Received time':val.strftime(" %d-%m-%Y"),'Keyword':key,'Subject':subject,'Url':url,'Title':arti,'Text_body':text_val},ignore_index=True,sort=False)
                                        logging.info(subject)
                                        #print("all the Urls:", urls)
                                        #print(table_data)

                            except:
                                continue
                            continue
                        continue
                #print(table_data.shape)
                #this the used to drag into next page of the mail
                wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id=":4"]/div[2]/div[1]/div/div[1]/div/div'))).click()
                time.sleep(3)
                    #table_data.to_csv("E:/googleAlert/res/googleAlert.csv")
            table_data.to_csv("E:/googleAlert/res/googleAlert_of"+str(value1_of_mail)+".csv")
            #this function call the Daily_Mail fi=unction that written above
            Daily_Mail()
            os.remove("E:/googleAlert/res/googleAlert_of"+str(value1_of_mail)+".csv")
            logging.info("E:/googleAlert/res/googleAlert_of"+str(value1_of_mail)+".csv  file deleted from the system after sending the data")
            T= False
        except:
            logging.info("problem in loading ,we are executing again this code ................")
            continue

import schedule
schedule.every().days.at("23:30").do(Job())
"""
This function  written to schedule the execution of the Job function. It will execute the job function every dat at 11:30 pm and send that mail to recipients.

"""
