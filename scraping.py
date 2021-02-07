#!/usr/bin/env python
# coding: utf-8

#Imports for Splinter/BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

executable_path = {'executable_path':"C://Users/Terence Lin/Documents/chromedriver/chromedriver.exe"}
browser = Browser('chrome',**executable_path,headless=False)

def mars_news(browser):

    #Vist mars NASA news webpage
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    
    #Delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide",wait_time=1)

    #Set up Html Parser
    html=browser.html
    news_soup = soup(html,'html.parser')

    #try/except for error handling
    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')
        #Use parent element to locate first 'a' tag and then save as 'news_title'
        news_title=slide_elem.find("div",class_='content_title').get_text()
        #Use the parent element to find paragraph text
        news_p=slide_elem.find("div",class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    ### Visit the URL
    url="https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html"
    browser.visit(url)

    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    #Parse resulting html with soup
    html = browser.html
    img_soup=soup(html,'html.parser')

    #Add try/except for error handling
    try:
        #Find relative image url
        img_url_rel = img_soup.find("img",class_="fancybox-image").get("src")

    except AttributeError:
        return None

    #Use base URL to create absolute URL
    img_url=f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'

    return img_url

def mars_facts():
    try:
        # use 'read_html' to scrape facts table and convert into dataframe
        df=pd.read_html('https://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # Assign columns and set index of dataframe
    df.columns=['description','value']
    df.set_index('description',inplace=True)

    #Convert datframe into HTML format, add bootstrap
    return df.to_html()

def scrape_all():
    # Initiate headless driver for deployment
    browser= Browser("chrome", executable_path="chromedriver", headless=True)
    
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions then store results to dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }

    #Stop webdriver and return the data
    browser.quit()
    return data

if __name__=="__main__":
    # If running as scrpit, print scraped data
    print(scrape_all())
