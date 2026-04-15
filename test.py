from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import pandas as pd

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.ebay.com/")
    page.wait_for_timeout(3000)

    # Input items into searchbox
    page.get_by_placeholder("Search for anything").fill("FANUC robot")

    page.get_by_placeholder("Search for anything").press("Enter")
    page.wait_for_timeout(3000)
    page.get_by_text("Sold Items").click()

    page.wait_for_timeout(3000)

     # Filtering Product above 2000$
    page.get_by_role("textbox", name="Min").fill("2000")
    page.get_by_role("textbox", name="Min").press("Enter")
    
    page.wait_for_timeout(3000)

    page.mouse.wheel(0, 800)
    browser.close()
  
