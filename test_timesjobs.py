import urllib.parse
from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
from playwright_stealth import Stealth

query = urllib.parse.quote("Python")
url = f"https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&txtKeywords={query}&txtLocation="

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    Stealth().apply_stealth_sync(page)
    try:
        page.goto(url, wait_until="domcontentloaded", timeout=20000)
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        cards = soup.find_all("li", class_="clearfix job-bx wht-shd-bx")
        print(f"Found {len(cards)} jobs on TimesJobs")
        if cards:
            title = cards[0].find("h2").find("a").text.strip()
            print(f"Title: {title}")
    except Exception as e:
        print(f"Failed: {e}")
    browser.close()
