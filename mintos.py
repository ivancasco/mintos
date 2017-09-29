import sys
import time
import os
import requests
import codecs
import re
from bs4 import BeautifulSoup
from contextlib import closing
from selenium import webdriver
from seleniumrequests import Chrome # pip install selenium
#from selenium.webdriver.support.ui import WebDriverWait
#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from sign.signdef import *
from pdb import set_trace as bp

class MI:
    def __init__(self):
        self.host = "https://www.mintos.com/en"
        self.user = os.environ['MINTOS_USER'] # export MINTOS_USER=mintosuser
        self.passwd = os.environ['MINTOS_PASS'] # export MINTOS_PASS=secret
        self.new_loans = []
        self.loan_last = 0
    def ts_exit(self, msg):
        sys.exit(time.strftime("%Y-%m-%d %H:%M:%S ") + str(msg))
    def getNewLoans(self):
        payload = {"_csrf_token": "7TOfAlMdEOAA2IvxkUJBd12Dy_vt7zLdI1HAXl5Hre0", "_username": self.user, "_password": self.passwd}
        options = webdriver.ChromeOptions()
        options.add_argument('headless')
        with closing(Chrome(chrome_options=options)) as browser:
            browser.request('POST', self.host + "/login/check", data = payload)
            browser.get(self.host + "/available-loans/primary-market/?sort_field=id&sort_order=DESC&max_results=100&page=1")
            page_source = browser.page_source # store it to string variable
        soup = BeautifulSoup(page_source, "html.parser") # response parsing
        # find primary market table
        rows = soup.find('table', {'id': 'primary-market-table'})
        if rows is not None:
            rows = rows.find('tbody').find_all('tr')
        pattern = re.compile("\d+")
        self.new_loans = []
        if rows is not None:
            for row in rows:
                cols = row.find_all('td')
                loan = int(pattern.search(cols[0].get_text()).group())
                if loan > self.loan_last:
                    self.new_loans.append(loan)
        if len(self.new_loans) > 0:
            self.loan_last = self.new_loans[0]

        return self.new_loans

#            button = browser.find_element_by_name('button')
#            button.click()
# wait for the page to load
#            WebDriverWait(browser, timeout=10).until(
#                lambda x: x.find_element_by_id('primary-market-table'))
