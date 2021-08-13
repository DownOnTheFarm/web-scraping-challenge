# Dependencies
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    
    # Mars News URL of page to be scraped
    MarsNews_url = 'https://mars.nasa.gov/news/'
    browser.visit(MarsNews_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    # Save Most Recent Article and Title 
    slidebar = soup.find('li', class_='slide')
    categories = slidebar.find_all('div', class_='content_title')
    for category in categories:
        news_title = category.text.strip()
    slidebar = soup.find('li', class_='slide')
    categories = slidebar.find_all('div', class_='article_teaser_body')
    for category in categories:
        news_p = category.text.strip()

    # Mars Image to be scraped
    base_url = 'https://spaceimages-mars.com/'
    featured_image_url = base_url + 'image/featured/mars1.jpg'
    browser.visit(featured_image_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    
    # Scrape Facts and Return Table in HTML
    facts_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(facts_url)
    facts_df = tables[1]
    facts_df.columns = ["Profile", "Value"]
    facts_df['Profile'] = facts_df['Profile'].str.replace(':', '')
    facts_html = facts_df.to_html()
    
    # Scrape Mars hemisphere title and image
    hemi_url='https://marshemispheres.com/'
    browser.visit(hemi_url)
    html=browser.html
    soup=bs(html,'html.parser')

    items = soup.find_all('div', class_='item')

    titles = []
    hemisphere_image_urls=[]
    for item in items:
        # Error handling
        try:
            # Extract title
            hem=item.find('div',class_='description')
            title=hem.h3.text
            # Extract image url
            hem_url=hem.a['href']
            browser.visit(hemi_url+hem_url)
            html=browser.html
            soup=bs(html,'html.parser')
            image_src=soup.find('li').a['href']
            if (title and image_src):
                # Print results
                print('-'*50)
                print(title)
                print(image_src)
            # Create dictionary for title and url
            hem_dict={
                'title':title,
                'image_url':hemi_url + image_src
            }
            hemisphere_image_urls.append(hem_dict)
        except Exception as e:
            print(e)
    print(hemisphere_image_urls)
    titles
    
    # Create dictionary for all info scraped from sources above
    mars_dict={
        "news_title":news_title,
        "news_p":news_p,
        "featured_image_url":featured_image_url,
        "fact_table":facts_html,
        "hemisphere_images":hemisphere_image_urls
    }
    # Close the browser after scraping
    browser.quit()
    return mars_dict
    