from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd


# Scrooling
def scroll_to_bottom(page, pause_time=2000):
    previous_height = 0

    while True:
        current_height = page.evaluate("document.body.scrollHeight")

        if current_height == previous_height:
            break

        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(pause_time)

        previous_height = current_height



with sync_playwright() as p:

    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.ebay.com/", wait_until="domcontentloaded")
    
    # Input items into searchbox
    page.get_by_placeholder("Search for anything").fill("FANUC robot")
    page.get_by_placeholder("Search for anything").press("Enter")
    page.wait_for_timeout(3000)
    # filtering by sold items
    page.mouse.move(0, 100)
    page.get_by_text("Sold Items").click()
    
    page.wait_for_timeout(4000)
    # Filtering Product above 2000$
    page.get_by_role("textbox", name="Min").fill("2000")
    page.get_by_role("textbox", name="Min").press("Enter")
    
    page.wait_for_timeout(3000)

    page.mouse.wheel(0, 800)
    page.on("response", lambda response: print(response.url))

    # page.wait_for_selector("#item3e47f12738")
    # robot_listing_html = page.content()
    # with open("robots_listing.html", "w", encoding='utf-8') as f:
    #     f.write(robot_listing_html)
    page.wait_for_timeout(3000)
    
    browser.close()