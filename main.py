import time
import json
import re
import random
import pandas as pd
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


# Function for extract each product details info
def extract_product_info(product_html):
    
    # Finding Product Content where all product info exits
    product_content = product_html.find("div",class_="su-card-container__content")
    
    product_details = {
        "product_title" : product_content.find("a", class_="s-card__link").find("div", class_="s-card__title").get_text(separator=" | "),

        "sold_date" : product_content.find("div", class_="s-card__caption").get_text(),
        
        "primary_container" : product_content.find("div", class_="su-card-container__attributes__primary").get_text(separator="||"),
        
        "secondary_container": product_content.find("div", class_="su-card-container__attributes__secondary").get_text(separator="||"),
        
        "product_image" : product_html.find("div",class_="su-card-container__media").find("a")["href"],
        
        "product_link" : product_content.find("a", class_="s-card__link")["href"]

    }

    return product_details


# Give row Rendered html to extract clean Data
def feed_html_get_data(html):
    soup = BeautifulSoup(html, "html.parser")
    product_lists = soup.find("ul", class_="srp-results srp-list clearfix").findAll("li", class_="s-card s-card--horizontal")

    all_product_details = []
    for product_html in product_lists:
        all_product_details.append(extract_product_info(product_html))

    return {"Faunc Robot" : all_product_details}

#------------------ Playwright Start----------------------
def Playwright_run_for_this(search_item):

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        page.goto("https://www.ebay.com/")
        page.wait_for_timeout(3000)
        
        # Enter search item into searchbox
        page.get_by_placeholder(text="Search for anything").fill(f"{search_item}")
        page.get_by_placeholder(text="Search for anything").press("Enter")
        page.mouse.wheel(0, 200)

        # filtering by sold items
        page.get_by_text("Sold Items").click()
        page.wait_for_timeout(3000)

        # Filtering Product above 2000$
        # page.get_by_label("Minimum Value in $").fill("2000")
        # page.get_by_label("Minimum Value in $").press("Enter")
        
        page.locator("input[aria-label='Minimum Value in $']").fill("2000") 
        page.locator("input[aria-label='Minimum Value in $']").press("Enter")

        page.wait_for_timeout(3000*2)
        for _ in range(1, random.randint(15, 20)):
            scrool_amount = random.randint(200, 600)
            page.mouse.wheel(0, scrool_amount)
            time.sleep(random.uniform(0.5, 2))
            
        html = page.content()
        data = feed_html_get_data(html)
        with open(f"_scraped_json\{search_item}.json", "w") as f:
            json.dump(data, f, indent=4)
        browser.close()


serach_data = pd.read_csv("search_terms.csv")
for i in (serach_data["Search This Exact Phrase"]):
    Playwright_run_for_this(i)
