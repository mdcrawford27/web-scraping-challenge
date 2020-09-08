from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd

def scrape():
    executable_path = {'executable_path': r'C:\Users\mdcra\chromedriver.exe'}
    browser = Browser("chrome", **executable_path, headless=False)

    news_title, news_p = news(browser)

    results = {
        "news_title": news_title,
        "news_p": news_p,
        "image": image(browser),
        "facts": facts(),
        "hemispheres": hemisphere_info(browser)
    }

    browser.quit()
    return results


def news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'lxml')


    try:
        article = soup.find('li', class_="slide")
        news_title = article.find('div', class_='content_title').get_text()
        news_p = article.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None,None

    return news_title, news_p

def image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    html = browser.html
    soup = bs(html, 'lxml')

    try:
        image = soup.find('article', class_='carousel_item').get("style")
        splits = image.split("'")
        url = splits[1]

    except AttributeError:
        return None

    featured_image_url = f'https://www.jpl.nasa.gov{url}'

    return featured_image_url

def facts():
    df = pd.read_html('https://space-facts.com/mars/')[0]
    df.columns=["Mars"," "]
    df.set_index("Mars", inplace=True)

    return df.to_html()

def hemisphere_info(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    hemispheres = []
    for i in range(4):
        hemi = {}
        hemi['title'] = browser.find_by_css("a.product-item h3").text
    
        browser.find_by_css("a.product-item h3")[i].click()
    
        sample= browser.links.find_by_text('Sample')
        hemi['img_url'] = sample['href']
  
        hemispheres.append(hemi)
        browser.back()

    return hemispheres  

if __name__ == "__main__":
    print(scrape())