from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import pymongo

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict ={}

    # Mars News URL of page to be scraped
    MarsNews_url = 'https://mars.nasa.gov/news/'
    browser.visit(MarsNews_url)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
   # Save Most Recent Article and Title 
    news_title = news_soup.find_all('div', class_='content_title')[0].text
    news_p = news_soup.find_all('div', class_='article_teaser_body')[0].text

    # Mars Image to be scraped
    base_url = 'https://spaceimages-mars.com/'
    featured_image_url = base_url + 'image/featured/mars1.jpg'
    browser.visit(featured_image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    print(featured_image_url)
    


    # Scrape Facts and Return Table in HTML
    facts_url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(facts_url)
    mars_facts_df = tables[2]
    mars_facts_df.columns = ["Profile", "Value"]
    mars_html_table = mars_facts_df.to_html()
    mars_html_table.replace('\n', '')
    
    