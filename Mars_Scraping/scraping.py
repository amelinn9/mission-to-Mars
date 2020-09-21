# import Splinter and BeautifulSoup, Pandas
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

# create a function that will initialise the browser, create a data dict, and end
# the WebDriver and return the scraped data
def scrape_all():
    # initialise headliss driver for deployment
    #executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser("chrome", executable_path="chromedriver", headless=False)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now(),
      "hemispheres": hemispheres(browser)
    }

    # Stop webdriver and return data
    browser.quit()
    return data


#############################################################################
# Scrape Article Title and Summaries
#############################################################################
# create a function to scrape titles and summaries
def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # search for elements with a specific combo of tag ul and li and attribute item_list and slide, respectively
    # Optional delay for loading the page (wait_time).
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # set up html parser (Convert the browser html to a soup object and then quit the browser)
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # add a try/except block to handle errors
    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        # Use the parent element to find the first 'a' tag and save it as 'news_title'-get_text returns only the text of the element
        news_title = slide_elem.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


################################################################################
# Scrape Featured Images
################################################################################
# create a function to scrape featured images
def featured_image(browser):
    # visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')[0]
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # add a try/except block to handle errors
    try: 
        # Find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")

    except AttributeError:
        return None

    # Use the base URL to create an absolute URL
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'

    return img_url


############################################################################
# Scrape Mars Facts
############################################################################
# create a function to scrape the entire table
def mars_facts():
    # add a try/except block to handle errors
    try:
        # scrape the entire table using pandas' read_html function into a df
        df = pd.read_html('http://space-facts.com/mars/')[0]

    except BaseException:
        return None

    # assign columns and set index of df
    df.columns=['Description', 'Mars']
    df.set_index('Description', inplace=True)

    # convert the dataframe back to html-ready code
    return df.to_html(classes="table table-striped")

if __name__ == "__main__":
    # if running as script, print scraped data
    print(scrape_all())


############################################################################
# Scrape Hemisphere Data
############################################################################
# create a function to scrape hemisphere data
def hemispheres(browser):
    # visit URL
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # create a list to hold the images and titles
    hemisphere_image_urls = []
    # set up html parser
    html = browser.html

    # add a try/except block to handle errors
    # CERBERUS
    cerb_page = browser.links.find_by_partial_text('Cerberus')
    cerb_page.click()
    html = browser.html
    cerb_soup = soup(html, 'html.parser')
    cerb_url = cerb_soup.select_one("div.downloads a").get("href")
    cerb_title = cerb_soup.select_one("h2", class_="title").get_text()

    cerberus_dict = {"img_url": cerb_url,
                    "title": cerb_title}


    # SCHIAPARELLI
    browser.visit(url)
    schia_page = browser.links.find_by_partial_text('Schiaparelli')
    schia_page.click()
    html = browser.html
    schia_soup = soup(html, 'html.parser')
    schia_url = schia_soup.select_one("div.downloads a").get("href")
    schia_title = schia_soup.select_one("h2", class_="title").get_text()

    schiaparelli_dict = {"img_url": schia_url,
                        "title": schia_title}


    # SYRTIS MAJOR
    browser.visit(url)
    syrt_page = browser.links.find_by_partial_text('Syrtis')
    syrt_page.click()
    html = browser.html
    syrt_soup = soup(html, 'html.parser')
    syrt_url = syrt_soup.select_one("div.downloads a").get("href")
    syrt_title = syrt_soup.select_one("h2", class_="title").get_text()

    syrtis_dict = {"img_url": syrt_url,
                "title": syrt_title}


    # VALLES MARINERIS
    browser.visit(url)
    val_page = browser.links.find_by_partial_text('Valles')
    val_page.click()
    html = browser.html
    val_soup = soup(html, 'html.parser')
    val_url = val_soup.select_one("div.downloads a").get("href")
    val_title = val_soup.select_one("h2", class_="title").get_text()

    valles_dict = {"img_url": val_url,
                "title": val_title}

    # append dicts to the list
    hemisphere_image_urls.append(cerberus_dict)
    hemisphere_image_urls.append(schiaparelli_dict)
    hemisphere_image_urls.append(syrtis_dict)
    hemisphere_image_urls.append(valles_dict)

    return hemisphere_image_urls
