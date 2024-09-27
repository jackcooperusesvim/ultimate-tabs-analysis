# Scraping and Analyzing Guitar Tabs (from Ultimate Guitar)

This is a project to scrape and analyze guitar tabs from [Ultimate Guitar](https://ultimate-guitar.com/).

## Data Acquisition

Scraping the data is done as a two-step process. First, my scraper will use Selenium to run a search through the tabs on the site to collect the links to all the individual tab endpoints. Then, using the simpler "requests" library, I will scrape each individual link for tabs, which will be stored in some sort of data-base.

