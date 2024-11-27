from selenium import webdriver
import requests
from icecream import ic
from selenium.webdriver.chrome.webdriver import WebDriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.common.by import By
from settings import *

import sqlite3
import bs4
import polars as pl
import time

def load_links(link_database: str = DEFAULT_LINK_DATABASE) -> pl.Series:
    with sqlite3.connect(link_database) as conn:
        df = pl.read_database("SELECT link from links",conn)
        return df["link"]

def create_webdriver(
        url: str,
    speedyboi: bool,
        wait: float = SECONDS_BETWEEN_REQUESTS,
        opts: Options = DEFAULT_WEB_DRIVER_OPTIONS
) -> WebDriver:
    web_driver = webdriver.Chrome(options = opts)
    ic("fetching url")
    web_driver.get(url)
    if speedyboi:
        ic("starting wait")
        web_driver.implicitly_wait(wait)
    ic("SPEEEEEEED")
    ic("done fetching url")
    return web_driver
def scrape_raw_tab(url: str, speedyboi = False) -> str:

    wd = create_webdriver(url, speedyboi=speedyboi)
    source = wd.page_source
    wd.close()

    name = url.split("tab/")[1]
    name = name.replace("/","_")


    with open(f"tabs/{name}.html",'w') as file:
        file.write(source)

    # tabs = source.split(f'style="font-size: 13px; font-family: &quot;Roboto Mono&quot;, &quot;Courier New&quot;, monospace;">')[0]
    # tabs = tabs.split(f'<div')[0]


    return source



if __name__ == "__main__":
