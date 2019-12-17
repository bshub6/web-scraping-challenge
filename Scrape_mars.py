
import time
import pandas as pd
from bs4 import BeautifulSoup
from splinter import Browser


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/webdrivers/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():

    browser = init_browser()

    mars_results = {}
    #Mar news scraping
   

    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(nasa_url)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    #print(soul.prettify())

    news_title = soup.find("div", class_="content_title").text
    news_paragraph = soup.find("div", class_="article_teaser_body").text

    print(f"Title: {news_title}")
    print(f"Para: {news_paragraph}")

    #Featured image url scraping

    image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(image_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    image = soup.find("img", class_="thumb")["src"]
    featured_image_url = "https://www.jpl.nasa.gov"+ image
    print(featured_image_url)

    #Mars weather tweet scraping
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)
    time.sleep(1)

    mars_weather_html = browser.html
    mars_weather_soup = BeautifulSoup(mars_weather_html, 'html.parser')

    tweets = mars_weather_soup.find('ol', class_="stream-items")
    mars_weather = tweets.find('p', class_="tweet-text").text
    print(mars_weather)

    #Mars Fact Scraping
    mars_facts_url ="https://space-facts.com/mars/"
    browser.visit(mars_facts_url)

    mars_data = pd.read_html(mars_facts_url)
    mars_data = pd.DataFrame(mars_data[0])

    mars_facts = mars_data.to_html(header = False, index = False)
    print(mars_facts)

    #Mars Hemisphere Photo Scraping
    base_hemisphere_url = "https://astrogeology.usgs.gov"
    hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemisphere_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    hemisphere_image_urls = []

    links = soup.find_all('div', class_='item')


    for link in links:
        img_dict = {}
        title = link.find("h3").text
        next_link = link.find('div', class_='description').a['href']
        full_next_link = base_hemisphere_url + next_link
            
        browser.visit(full_next_link)
        
        pic_html = browser.html
        pic_soup = BeautifulSoup(pic_html, 'html.parser')
        url = pic_soup.find('img', class_='wide-image')['src']
            
        img_dict['title'] = title
        img_dict['img_url'] = base_hemisphere_url + url
        print(img_dict['img_url'])
            
        hemisphere_image_urls.append(img_dict)
        
        browser.quit()
        
    return hemisphere_image_urls

    

