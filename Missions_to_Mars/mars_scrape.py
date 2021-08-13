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
    news_title = news_soup.find_all('div', class_='content_title').text
    news_p = news_soup.find_all('div', class_='article_teaser_body').text

    # Mars Image to be scraped
    base_url = 'https://spaceimages-mars.com/'
    featured_image_url = base_url + 'image/featured/mars1.jpg'
    browser.visit(featured_image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    
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

    urls = []
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
    