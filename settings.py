from selenium.webdriver.chrome.options import Options

DEFAULT_WEB_DRIVER_OPTIONS = Options()
DEFAULT_WEB_DRIVER_OPTIONS.add_argument("--headless=new")

SECONDS_BETWEEN_REQUESTS = 1
MENU_URL = "https://www.ultimate-guitar.com/explore?capo[]=0&live[]=0&page=100&part[]=&tuning[]=1&type[]=Tabs"
DEFAULT_LINK_DATABASE = "links.db"
USE_LAST_LINK = True
LAST_LINK_PATH = "logs/last_link.txt"

