from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.safari.options import Options as SafariOptions


Options = ChromeOptions | SafariOptions | FirefoxOptions

DEFAULT_WEB_DRIVER =  "firefox"

DEFAULT_WEB_DRIVER_OPTIONS = FirefoxOptions()

SECONDS_BETWEEN_REQUESTS = 10
MENU_URL = "https://www.ultimate-guitar.com/explore?order=hitstotal_desc&type%5B%5D=Tabs"
DEFAULT_LINK_DATABASE = "source/links2.db"
USE_LAST_LINK = True
LAST_LINK_PATH = "logs/last_link.txt"
