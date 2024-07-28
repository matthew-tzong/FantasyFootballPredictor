import os
import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeout


"""
The code is designed to scrape game log and box score data from the Pro-Football-Reference website for the 2020-2023 NFL Seasons. 
It retrieves and saves HTML data from various pages, organizing the data into a folder of HTML files for further analysis.
"""


#Folder to store box score HTML files
boxScoreDirectory = "data/scores"


async def getHTMLData(url, selector, sleep=5, retries=3):
    """
    Fetches all href attributes from elements matching the selector for the URL

    Arguments:
        URL (str): The URL to fetch data from.
        Selector (str): The CSS selector to locate elements.
        Sleep (int): The base time to wait between retries.
        Retries (int): # of retries in case of failure.

    Returns:
        List: List of href attributes extracted from the page.
    """
    hrefs = []
    for i in range(retries):
        await asyncio.sleep(sleep * i)       # Wait longer each time in between failures to not overload the page
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)    # Used headless browser to run faster
                page = await browser.new_page()
                await page.goto(url, timeout = 30000)      # Navigate to URL
                elements = await page.query_selector_all(selector)  # Find elements matching selector
                for element in elements:
                   href = await element.get_attribute('href')   # Get href attribute, if it exists then append
                   if href:
                       hrefs.append(href)
                await browser.close()         # Close Browser
        except PlaywrightTimeout:
            print(f"Timeout Error on {url}")
            continue  # Retry if timeout
        else:
            break # Exit loop if successful
    return hrefs

async def getUpdatedHTML(url, selector, sleep=5, retries=3):
    """
    Fetch inner HTML of element matching the selector for the URL

    Arguments:
        URL (str): The URL to fetch data from.
        Selector (str): The CSS selector to locate elements.
        Sleep (int): The base time to wait between retries.
        Retries (int): # of retries in case of failure.

    Returns:
        str: Inner HTML element if successful else None
    """
    html = None
    for i in range(retries):
        await asyncio.sleep(sleep * i)  # Wait longer each time in between failures to not overload the page
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)  # Used headless browser to run faster
                page = await browser.new_page()
                await page.goto(url, timeout = 30000)  # Navigate to URL
                html = await page.inner_html(selector)  # Find element matching selector
        except PlaywrightTimeout:
            print(f"Timeout Error on {url}")
            continue  # Retry if timeout
        else:
            break   # Exit loop if successful
    return html

async def scrapeSeason(season):
    """
    Scrapes game logs for each given season from each NFL team

    Args:
        Season (int): The season year to scrape.
    """
    hrefs = set()
    # List of all team abbreviations in URL
    teams = ["sea", "buf", "rav", "min", "cin", "pit", "phi", "oti", "nyj", "atl", "crd", "htx", "mia", "car", "sfo", "den", "det", "gnb", "chi", "cle", "jax", "kan", "rai", "nor", "ram", "was", "nwe", "tam", "dal", "clt", "nyg", "sdg"]
    for team in teams:
        # Construct the URL for each team's game log for the given season
        url = f"https://www.pro-football-reference.com/teams/{team}/{season}/gamelog/"
        selector = f"#gamelog{season} .center a"      # CSS selector to locate the game's box score links
        hrefs.update(await getHTMLData(url, selector))   # Collect game links
    # Construct the full URLs for box score pages
    boxScorePages = [f"https://www.pro-football-reference.com/{l}" for l in hrefs]
    for url in boxScorePages:
        filename = url.split("/")[-1]   # Extract filename from URL
        save_path = os.path.join(boxScoreDirectory, filename)     # Define path to save HTML file
        if os.path.exists(save_path):   # Skip if path already exists
            continue
        html = await getUpdatedHTML(url, "#player_offense")    # Fetch HTML of the box score table
        if not html:
            print(f"no html found for {url}")   # Print message if no HTML is found
            continue
        with open(save_path, "w+") as f:
            f.write(html)    # Save the HTML content to file
    print(os.listdir(boxScoreDirectory))



seasons = list(range(2020, 2024))  # Define the range of seasons
for season in seasons:
    scrapeSeason(season)         # Scrape data for each season
    print(f"finished {season}")
print("done")
    

