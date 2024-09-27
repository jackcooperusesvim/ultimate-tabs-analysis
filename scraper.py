from os import link
from selenium import webdriver
from icecream import DEFAULT_OUTPUT_FUNCTION, ic
from selenium.webdriver.chrome.webdriver import WebDriver as ChromeWebDriver
from selenium.webdriver.common import options
from selenium.webdriver.safari.webdriver import WebDriver as SafariWebDriver
from selenium.webdriver.firefox.webdriver import WebDriver as FirefoxWebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.safari.options import Options as SafariOptions

import sqlite3
import bs4
import polars as pl
import time

WebDriver = ChromeWebDriver | SafariWebDriver | FirefoxWebDriver
Options = ChromeOptions | SafariOptions | FirefoxOptions
DEFAULT_WEB_DRIVER = "firefox"

DEFAULT_WEB_DRIVER_OPTIONS = FirefoxOptions()

SECONDS_BETWEEN_REQUESTS = 10
MENU_URL = "https://www.ultimate-guitar.com/explore?order=hitstotal_desc&type%5B%5D=Tabs"
DEFAULT_LINK_DATABASE = "source/links2.db"
LAST_LINK = "logs/last_link.txt"
def build_db(link_database: str = DEFAULT_LINK_DATABASE) -> None:
    with sqlite3.connect(link_database) as conn:
        conn.execute("CREATE TABLE IF NOT EXISTS links (id INTEGER PRIMARY KEY, link TEXT UNIQUE )")
        conn.commit()

def save_links(links: list[str], link_database: str = DEFAULT_LINK_DATABASE):
    with sqlite3.connect(link_database) as conn:
        for link in links:
            try:
                conn.execute("INSERT INTO links(link) VALUES (?)", (link,))
            except sqlite3.IntegrityError as e:
                ic(e)
                ic("link already exists")

        conn.commit()

def load_links(link_database: str = DEFAULT_LINK_DATABASE) -> pl.Series:
    with sqlite3.connect(link_database) as conn:
        df = pl.read_database("SELECT link from links",conn)
        return df["link"]

def create_webdriver(url: str, driver: str = DEFAULT_WEB_DRIVER, wait: float = SECONDS_BETWEEN_REQUESTS, opts:Options = DEFAULT_WEB_DRIVER_OPTIONS) -> WebDriver:
    match driver:
        case "safari":
            web_driver = webdriver.Safari(options = opts)
        case "chrome":
            web_driver = webdriver.Chrome(options = opts)
        case "firefox":
            web_driver = webdriver.Firefox(options = opts)
        case _:
            raise Exception(f"invalid driver: {driver}")

    ic("fetching url")
    web_driver.get(url)
    ic("starting wait")
    web_driver.implicitly_wait(wait)
    ic("done fetching url")
    return web_driver

def get_links_from_source(source: str) -> list[str]:
    soup = bs4.BeautifulSoup(source, "html.parser")
    links = soup.find_all("a")
    try:
        links = [link.get("href") for link in links if ("tabs.ultimate-guitar.com/tab" in link.get("href"))]
    except:
        links = [link.get("href") for link in links if ("tab" in link.get("href"))]
    return links

def scrape_raw_tab_menu(web_driver: WebDriver, save: bool) -> tuple[WebDriver, list[str], str]:
    source = web_driver.page_source
    if save:
        with open(f"source/raw_menu.html",'w') as file:
            file.write(source)

    tab_links = get_links_from_source(source)

    return web_driver, tab_links, source

def next_page(web_driver: WebDriver) -> WebDriver:
    # Is it inefficient? Yes. idrc tbh tho.
    soup = bs4.BeautifulSoup(web_driver.page_source, "html.parser")
    anchors = soup.find_all('a')
    anchor = [a for a in anchors if ("next >" in a.contents)][0]
    element = web_driver.find_element(By.XPATH, f"//a[@href='{anchor['href']}']")

    if element is not None:
        element.click()

    ic(len(anchors))
    time.sleep(SECONDS_BETWEEN_REQUESTS)
    return web_driver

def scrape_raw_tab(url: str, driver: str = DEFAULT_WEB_DRIVER) -> str:

    web_driver = create_webdriver(url, driver)

    web_driver.get(url)

    source = web_driver.page_source
    name = url.split("tab/")[1]
    name = name.replace("/","_")


    with open(f"source/{name}.html",'w') as file:
        file.write(source)

    # tabs = source.split(f'style="font-size: 13px; font-family: &quot;Roboto Mono&quot;, &quot;Courier New&quot;, monospace;">')[0]
    # tabs = tabs.split(f'<div')[0]

    web_driver.close()

    return source

if __name__ == "__main__":
    counter = 0
    with open(LAST_LINK,'r') as file:
        last_link = file.read()

    build_db()

    wd = create_webdriver(url = MENU_URL)
    try:
        while True:

            for _ in range(10):
                print("starting new page")
                save_links(get_links_from_source(wd.page_source))

                while True:
                    try:
                        wd = next_page(wd)
                        break

                    except Exception as e:
                        print(e)
                        print("deleting cookies")
                        wd.delete_all_cookies()
                        with open(f"logs/err.txt",'w') as file:
                            file.write(wd.page_source)
                        time.sleep(1)

                with open(LAST_LINK,'w') as file:
                    file.write(wd.current_url)
                print(counter)
            print("sleeping...")
            time.sleep(4)
    except Exception as e:
        ic(e)
        input("press enter to close browser")
        wd.close()
        raise e 
    # for tab_link in tab_links:
    #     scrape_raw_tab(tab_link)
    #     time.sleep(SECONDS_BETWEEN_REQUESTS)

