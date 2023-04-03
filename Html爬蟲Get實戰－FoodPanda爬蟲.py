# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 09:33:25 2021

@author: Ivan
課程教材：行銷人轉職爬蟲王實戰｜5大社群平台＋2大電商
版權屬於「楊超霆」所有，若有疑問，可聯絡ivanyang0606@gmail.com

第一章 爬蟲基本訓練
Html爬蟲實戰－FoodPanda爬蟲
"""
from bs4 import BeautifulSoup
import pandas as pd
#2023/4/3 因foodpanda加入機器人驗證機制，因此無法再使用BeautifulSoup進行爬蟲
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time


# 自動下載ChromeDriver
service = ChromeService(executable_path=ChromeDriverManager().install())

# 關閉通知提醒
chrome_options = webdriver.ChromeOptions()
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)

# 開啟瀏覽器
driver = webdriver.Chrome(service=service, chrome_options=chrome_options)
time.sleep(5)

# 開啟網頁
driver.get('https://www.foodpanda.com.tw/en/city/taipei-city' )
time.sleep(10)

# 滾動頁面
for scroll in range(6):
    driver.execute_script('window.scrollBy(0,1000)')
    time.sleep(2)
    
#將整個網站的程式碼爬下來
soup = BeautifulSoup(driver.page_source, "html.parser")
getall = soup.findAll('figcaption',{'class':'vendor-info'}) #取得所有店家
i = getall[0] # 先看第一個商店

print(i.find('span',{'class':'name'}).text) #取得店家名稱
print(i.find('span',{'class':'rating--label-primary'}).text) #取得評分 2023/4/3修改
print(i.find('li',{'class':'vendor-characteristic'}).text) #取得標籤


# 整理成資料表
shopName = []
star = []
tag = []
shipping = []
for i in getall:
    shopName.append(i.find('span',{'class':'name'}).text)
    # 有可能會沒有星等評分，因此需要檢查
    getStart = i.find_all('span',{'class':'rating--label-primary'})
    if len(getStart) > 0:
        star.append(getStart[0].text)
    else:
        star.append('無資料')
    tag.append(i.find('li',{'class':'vendor-characteristic'}).text)

    
pd.DataFrame({
    '店家名稱':shopName,
    '評分':star,
    '標籤':tag
    }).to_csv('foodpanda.csv', encoding='utf-8-sig', index=False)
