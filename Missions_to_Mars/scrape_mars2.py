# Dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import pandas as pd
import os
import re
import requests
import time

def scrape():
    if os.name=="nt":
     executable_path = {'executable_path': './chromedriver.exe'}
    else:
     executable_path = {"executable_path": "/usr/local/bin/chromedriver"}

    browser = Browser('chrome', **executable_path, headless=False)

    #NASA Mars News
#Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text. 
#Assign the text to variables that you can reference later.



    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)


    # In[ ]:


    # Iterate through all pages
        # HTML object
    html = browser.html
        # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
        # Retrieve all elements that contain article information 
    articles = soup.find("div", class_='list_text')
    # Use Beautiful Soup's find() method to navigate and retrieve attributes
    news_title = articles.find("div", class_="content_title").text
    news_p = articles.find("div", class_ ="article_teaser_body").text
    


    # ### JPL Mars Space Images - Featured Image

    # In[ ]:
        
    url_jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_jpl)


    # In[ ]:


    #Use splinter to navigate the site and Click Button with Class Name full_image to
    #find the image url for the current Featured Mars Image
    full_image_button = browser.find_by_id("full_image")
  
    full_image_button.click()

    time.sleep(10)
    # In[ ]:


    # Find "More Info" Button and Click It to get to the large image of the current
    #Featured Mars Image
    more_info_element = browser.links.find_by_partial_text("more info")
    more_info_element.click()


    # HTML object
    html_jpl = browser.html
    # Parse HTML with Beautiful Soup
    soup_jpl = BeautifulSoup(html_jpl, 'html.parser')



    #Get the full image details
    image = soup_jpl.select_one("figure.lede a img").get("src")
   

    #pull together full url
    featured_image_url = 'https://www.jpl.nasa.gov' + image

    # ### Mars Weather


    # URL of page to be scraped
    url = 'https://twitter.com/marswxreport?lang=en'


    # Retrieve page with the requests module
    response = requests.get(url)


    # Create BeautifulSoup object; parse with 'html.parser'
    soup = BeautifulSoup(response.text, 'html.parser')

    # Examine the results, then determine element that contains sought info
    #print(soup.prettify())


    mars_weather = soup.find("p", class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
    #print(mars_weather)


    # ### Mars Facts



    # URL of page to be scraped
    facts_url = 'https://space-facts.com/mars/'


    # In[ ]:


    fact_table = pd.read_html(facts_url)
    fact_table[0]

    mars_facts = fact_table[0]
    mars_facts.columns = ["Facts", "Values"]
    mars_facts.set_index(["Facts"])

    mars_facts_html = mars_facts.to_html()
    mars_facts_html
    mars_facts.to_html('mars_fact_table.html')

    # ### Mars Hemisphere

    url_hemi = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hemi)


    # HTML object
    html_hemi = browser.html
    # Parse HTML with Beautiful Soup
    soup_hemi = BeautifulSoup(html_hemi, 'html.parser')

    mars_hemi_info = []

    # Get a List of All the Hemispheres
    links = browser.find_by_css("a.product-item h3")
    for link in range(len(links)):
        hemisphere = {}
        
        # Find Element on Each Loop to Avoid a Stale Element Exception
        browser.find_by_css("a.product-item h3")[link].click()
        
        # Find Sample Image Anchor Tag & Extract <href>
        sample_link = browser.links.find_by_text("Sample").first
        hemisphere["img_url"] = sample_link["href"]
        
        # Get Hemisphere Title
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # Append Hemisphere Object to List
        mars_hemi_info.append(hemisphere)
        
        # Navigate Backwards
        browser.back()

    mars_data = {
        "news_title": news_title,
        "news_paragraph": news_p,
        "featured_image": featured_image_url,
        "weather": mars_weather,
        #"facts": mars_facts,
        "hemispheres": mars_hemi_info,
           }
    browser.quit()

    return mars_data 



