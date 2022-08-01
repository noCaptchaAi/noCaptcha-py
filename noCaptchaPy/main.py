import requests
import selenium
import time
import undetected_chromedriver as uc
from selenium import webdriver
import re, requests, json
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    ElementNotVisibleException,
    ElementClickInterceptedException,
    WebDriverException,
    TimeoutException,
)

options = webdriver.ChromeOptions()
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')


class nocap:
    def __init__(self, uid: str, apikey: str):
        self.uid = uid
        self.apikey = apikey
        self.api_url = 'https://solve.shimul.me/api/solve'
    def solve(self, site_url: str, method: str):
        if site_url == "":
            site_url = "https://shimuldn.github.io/hCaptchaSolverApi/demo_data/demo_sites/2/"
        if method == "browser":
            driver = uc.Chrome(options=options, use_subprocess=True)
            driver.get(site_url)
        elif method == "requests":
            session = requests.Session()
            res = session.get(site_url)
            print(res.status_code)
        else:
            print("Invalid method available methods: browser, requests")
            return False
            