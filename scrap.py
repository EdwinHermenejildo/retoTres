from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service

import time

URL = 'http://www.pbclibrary.org/raton/mousercise.htm'

class Navigator:
    def __init__(self):
        breakpoint()
        self.service = Service('./chromedriver')
        self.service.start()
        self.driver = webdriver.Remote(self.service.service_url)

    def call(self):
        self.driver.get(URL)

        for idx in range(0, 30):
            time.sleep(0.5)
            try:
                print(idx)
                if idx == 0:
                    self.rules().get('start')()
                    continue

                if idx >= 9 and idx < 22:
                    self.rules().get('page-by_index')(idx)
                    continue

                if idx >= 22 and idx < 24:
                    self.rules().get('click-all-elements')()
                    continue

                if idx == 24:
                    self.rules().get('page-24')()
                    continue

                self.rules().get('default')()
            except Exception as e:
                self.fallback()

    def call_default_rule(self):
        element = self.driver.find_element(By.XPATH, "//input")
        element.click()

    def call_anchor_navigate(self):
        element = self.driver.find_element(By.CSS_SELECTOR, "a.bigger")
        element.click()

    def fallback(self):
        try:
            element = self.driver.find_element(By.XPATH, "//input | //a | //button")
            element.click()
        except NoSuchElementException:
            print('Unkown error - failing')


    def page_by_idx(self, idx):
        element = self.driver.find_element(By.XPATH, "//a[contains(text(), '{}')]".format(str(idx)))
        element.click()

    def page_24(self):
        elements = self.driver.find_elements(By.XPATH, "//input | //a | //button | //img")
        for element in elements:
            ActionChains(self.driver).double_click(element).perform()



        try:
            element = self.driver.find_element(By.XPATH, "//input | //a | //button")
            element.click()
        except NoSuchElementException:
            print('Unkown error - failing')

    def click_all_elements(self):
        elements = self.driver.find_elements(By.XPATH, "//input | //a | //button | //img")
        for element in elements:
            element.click()

        try:
            element = self.driver.find_element(By.XPATH, "//input | //a | //button")
            element.click()
        except NoSuchElementException:
            print('Unkown error - failing')


    def rules(self):
        return {
            "start": self.call_default_rule,
            "default": self.call_anchor_navigate,
            "page-by_index": self.page_by_idx,
            "page-24": self.page_24,
            "click-all-elements": self.click_all_elements,
            }


navigator = Navigator()
navigator.call()

