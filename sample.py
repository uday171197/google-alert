from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
from newspaper import Article
import newspaper

driver = webdriver.Chrome(executable_path="C:\Drivers\chromedriver.exe")
driver.get("https://accounts.google.com/signin/v2/identifier?continue=https%3A%2F%2Fmail.google.com%2Fmail%2F&service=mail&sacu=1&rip=1&flowName=GlifWebSignIn&flowEntry=ServiceLogin")
mail_path = driver.find_element_by_xpath('//*[@id="identifierId"]')
mail_path.send_keys("standardbk.alerts@gmail.com")
driver.find_element_by_xpath('//*[@id="identifierNext"]').click()
time.sleep(5)
wait = WebDriverWait(driver, 20)
try:
    password = wait.until(EC.element_to_be_clickable((By.NAME,'password'))).send_keys("passwd@123")
    driver.find_element_by_xpath('//*[@id="passwordNext"]').click()
    time.sleep(5)
except:
    print("Error in password loading")

#table declearation
import pandas as pd
Top=['Received time','Subject','Url','Title','Text_body']
table_data=pd.DataFrame()# we create a empty dataframe
table_data=pd.DataFrame(columns=Top)

table_id1=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id=":2v"]'))).click()
html_news=driver.page_source
soup1=BeautifulSoup(html_news,'html.parser')
table1=soup1.find("table", { "class":"Bs nH iY bAt"})
row1=table1.findChildren(['tr'])

row1=table1.findChildren(['tr'])
#print(row1)
urls=[]
T = True
while T == True:
    #print(i)
    url=''
    atri= None
    text_body=[]
    try:
        result = str(i).index('url=https:www.//')
        b=str(i)
        for i in range(result+4,result+200) break  if b[i] =='&' else: url=url+b[i]
        if url not in urls:
                article = Article(url)
                article.download()
                Articles=BeautifulSoup(article.html,'html.parser')
                arti=Articles.title.string
                print(arti)
                if arti != None:
                    sina_paper = newspaper.build(url,language='en')
                    article = sina_paper.articles[1]
                    article.download()
                    article.parse()
                    text_val= article.text
                    table_data = table_data.append({'Received time':' 08-08-2019 ,08:00AM','Subject':'Google Alert â€“ Daily Digest','Url':url,'Title':atri,'Text_body':text_val},ignore_index=True,sort=False)
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
                    table_data = table_data.append({'Received time':' 08-08-2019 ,08:00AM','Subject':'Google Alert â€“ Daily Digest','Url':url,'Title':atri,'Text_body':text_val},ignore_index=True,sort=False)
        except:
            continue
        T=False
        continue

table_data.to_csv("E:/googleAlert/res/googleAlerts_sample2.csv")
print(len(text_body))
