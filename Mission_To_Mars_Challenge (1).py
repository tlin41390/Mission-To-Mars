#!/usr/bin/env python
# coding: utf-8

# In[2]:


#Imports for Splinter/BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[3]:


#Set the executable path and initialize chrome browser in splinter
executable_path = {'executable_path':"C://Users/Terence Lin/Documents/chromedriver/chromedriver.exe"}
browser = Browser('chrome',**executable_path,headless=False)


# In[4]:


#Visst mars NASA news webpage
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
#Delay for loading the page
browser.is_element_present_by_css("ul.item_list li.slide",wait_time=1)


# In[5]:


#Set up Html Parser
html=browser.html
news_soup = soup(html,'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[6]:


slide_elem.find("div",class_='content_title')


# In[7]:


#Use parent element to locate first 'a' tag and then save as 'news_title'
news_title=slide_elem.find("div",class_='content_title').get_text()
news_title


# In[8]:


#Use parent element to find the paragraph text
news_p=slide_elem.find("div",class_="article_teaser_body").get_text()
news_p


# ### Featured Images
# 

# In[9]:


### Visit the URL
url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
browser.visit(url)


# In[10]:


#Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[11]:


#Parse resulting html with soup
html = browser.html
img_soup=soup(html,'html.parser')


# In[12]:


#Find relative image url
img_url_rel = img_soup.find("img",class_="fancybox-image").get("src")
img_url_rel


# In[13]:


#Use base URL to create absolute URL
img_url=f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# In[14]:


df=pd.read_html('https://space-facts.com/mars/')[0]
df.columns=['description','value']
df.set_index('description',inplace=True)
df


# In[15]:


df.to_html()


# In[16]:


# Visit the weather website
url = 'https://mars.nasa.gov/insight/weather/'
browser.visit(url)


# In[17]:


# Parse the data
html = browser.html
weather_soup = soup(html, 'html.parser')


# In[18]:


# Scrape the Daily Weather Report table
weather_table = weather_soup.find('table', class_='mb_table')
print(weather_table.prettify())


# In[134]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[138]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

html=browser.html
hemisphere_soup = soup(html,'html.parser')
for n in range(4):
    thumbnail =browser.find_by_tag('h3')[n]
    thumbnail.click()
    
    html=browser.html
    hemisphere_soup = soup(html,'html.parser')
    
    url = hemisphere_soup.find("li")
    title = hemisphere_soup.find("h2",class_="title").get_text()
    hemisphere_url=url.find("a").get('href')
    
    data = {"url":hemisphere_url,
            "title":title}
    hemisphere_image_urls.append(data)
    browser.back()
# 3. Write code to retrieve the image urls and titles for each hemisphere.


# In[139]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[140]:


# 5. Quit the browser
browser.quit()


# In[ ]:




