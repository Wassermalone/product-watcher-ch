from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import re
import datetime

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(options=options, executable_path="chromedriver.exe")

driver.get("https://www.ricardo.ch/")

search = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div/form/div/div/div[1]/input")
search.send_keys("SSD")

button = driver.find_element_by_xpath("/html/body/div[1]/div/div[3]/div/div/form/button")
button.click()


items = []

ids = driver.find_elements_by_class_name('card--3OWgD')
i = 0
for item in ids:
    # Split all card text into a list of strings
    lines = item.text.split('\n')

    # Get auction title
    article_title = lines[1]

    # Extract time as datetime obj
    end_date = datetime.datetime.strptime(lines[2], '%d. %b. %Y, %H:%M')

    # Remove unnecessary information
    while ("Neu eingestellt" in lines):
        lines.remove("Neu eingestellt")

    # print(lines)

    auction = {}
    num_bids = None
    cur_bid = None
    buy_price = None

    for i, item in enumerate(lines):
        if i == 0:
            previous_item = None
        else:
            previous_item = lines[i - 1]

        if i == len(lines) - 1:
            next_item = None
        else:
            next_item = lines[i + 1]

        # Check that previous_item isn't NoneType
        if previous_item:
            if "Gebote" in previous_item:
                num_bids = int(previous_item.split(' ')[0])
                cur_bid = float(item)
            if "Sofort kaufen" in previous_item:
                buy_price = float(item)

    # Auction & direct
    if (type(num_bids) is int) and buy_price:
        auction = {'type': 'hybrid', 'title': article_title, 'num_bids': num_bids, 'cur_bid': cur_bid,
                   'buy_price': buy_price, 'end_date': end_date}
    # Only direct
    elif buy_price:
        auction = {'type': 'direct', 'title': article_title, 'buy_price': buy_price, 'end_date': end_date}

    # Only auction
    else:
        auction = {'type': 'auction', 'title': article_title, 'num_bids': num_bids, 'cur_bid': cur_bid,
                   'end_date': end_date}

    print(auction)

    print('')



driver.quit()
