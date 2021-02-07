#!/usr/bin/env python
# coding: utf-8

#Imports for Splinter/BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

executable_path = {'executable_path':"C://Users/Terence Lin/Documents/chromedriver/chromedriver.exe"}
browser = Browser('chrome',**executable_path,headless=False)

#Visst mars NASA news webpage
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
#Delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide",wait_time=1)

#Set up Html Parser
html=browser.html
news_soup = soup(html,'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')
slide_elem.find("div",class_='content_title')

#Use parent element to locate first 'a' tag and then save as 'news_title'
news_title=slide_elem.find("div",class_='content_title').get_text()
news_title

news_p=slide_elem.find("div",class_="article_teaser_body").get_text()
news_p

### Visit the URL
url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
browser.visit(url)

full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

#Parse resulting html with soup
html = browser.html
img_soup=soup(html,'html.parser')

#Find relative image url
img_url_rel = img_soup.find("img",class_="fancybox-image").get("src")
img_url_rel

#Use base URL to create absolute URL
img_url=f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url

df=pd.read_html('https://space-facts.com/mars/')[0]
df.head()

df.columns=['description','value']
df.set_index('description',inplace=True)
df

df.to_html()

browser.quit()
