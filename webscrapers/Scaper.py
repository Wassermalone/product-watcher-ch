from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import datetime

from abc import ABC, abstractmethod

class Scraper(ABC):

    def __init__(self, website):
        super().__init__()

        self.website = website

        self.options = Options()
        self.options.headless = False
        self.options.add_argument("--window-size=1920,1080")

        self.driver = webdriver.Chrome(options=self.options, executable_path='chromedriver.exe')


    @abstractmethod
    def get_products(self):
        pass







