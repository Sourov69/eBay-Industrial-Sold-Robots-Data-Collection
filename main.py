import time
import json
import re
import random
from playwright.sync_api import sync_playwright



with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    page.goto("https://www.ebay.com/")
    page.wait_for_timeout(3000)
    
    # Enter search item into searchbox
    page.get_by_placeholder(text="Search for anything").fill("FANUC robot")
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

    page.wait_for_timeout(3000*3)
    for _ in range(1, 10):
        scrool_amount = random.randint(200, 600)
        page.mouse.wheel(0, scrool_amount)
        time.sleep(random.uniform(0.5, 2))
        
    html = page.content()
    with open("page.html", "w", encoding="utf-8") as f:
        f.write(html)
    browser.close()