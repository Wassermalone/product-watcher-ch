from webscrapers.Scaper import Scraper
import datetime
from tabulate import tabulate
import itertools
import csv


# CSV title, type, num_bids, cur_bid, buy_price, end_date, link

class RicardoScraper(Scraper):
    def get_products(self):
        found = self.remove_duplicates(self.go_through_categories())

        self.driver.quit()
        # print(tabulate(found, headers=["Title", "Type", "Num Bids", "Current Bid", "Buy Price", "End Date", "Link"]))

        # name of csv file
        filename = "auctions.csv"

        fields = ["Title", "Type", "Num Bids", "Current Bid", "Buy Price", "End Date", "Link"]

        # writing to csv file
        with open(filename, 'w', newline='') as csvfile:
            # creating a csv writer object
            csvwriter = csv.writer(csvfile)

            # writing the fields
            csvwriter.writerow(fields)

            # writing the data rows
            csvwriter.writerows(found)


    def go_through_categories(self, path='ActiveCategories.txt'):
        products = []
        file = open(path, 'r')
        for line in file:
            products.extend(self.get_products_from_first_page(line))

        return products



    def get_products_from_first_page(self, page):
        products = []
        i = 1
        while (True):
            # Hop to next page
            self.driver.get('%s?page=%d' % (page, i))
            i += 1

            page_products = self.get_products_from_page()

            count = 0
            for product in page_products:
                if product in products:
                    count += 1



            products.extend(page_products)

            # Stop when there's only one element left i.e. when we hit last page
            if len(page_products) < 15 or count > 15:
                return products

        # remove duplicates from list of lists
        return products

    def remove_duplicates(self, list):
        links = []
        cleaned_list = []
        for entry in list:
            if entry[-1] not in links:
                links.append(entry[-1])
                cleaned_list.append(entry)

        return cleaned_list

    def get_products_from_page(self):
        # ids = self.driver.find_elements_by_class_name('card--3OWgD')
        ids = self.driver.find_elements_by_class_name('MuiGrid-grid-md-3')
        auction_list = []
        links = []

        for item in ids:
            # Split all card text into a list of strings
            lines = item.text.split('\n')

            # TODO: Testen ob nur Artikel mit leerem Titel geprinted werden
            if (len(lines) == 7 and 'Neu eingestellt' in lines):
                print("Anomalie: ", lines)
                continue

            article_link = item.get_attribute("href")
            # Get auction title
            article_title = lines[1]

            # Extract time as datetime obj
            time_bar = lines[2]
            if ('Angebot beendet' in time_bar):  # when it just ended
                end_date = datetime.datetime.now()
            elif ('Noch' not in time_bar):  # get date when auction ends
                end_date = datetime.datetime.strptime(lines[2], '%d. %b. %Y, %H:%M')
            else:  # special case when listing goes into last hour
                end_date = datetime.datetime.now() + datetime.timedelta(minutes=float(time_bar.split(' ')[1]))

            # Remove unnecessary information
            while ("Neu eingestellt" in lines):
                lines.remove("Neu eingestellt")

            num_bids = None
            cur_bid = None
            buy_price = None

            for i, item in enumerate(lines):
                if i == 0:
                    previous_item = None
                else:
                    previous_item = lines[i - 1]

                # Check that previous_item isn't NoneType
                if previous_item:
                    if "Gebote" in previous_item:
                        num_bids = int(previous_item.split(' ')[0])
                        cur_bid = float(item.replace('\'', ''))
                    if "Sofort kaufen" in previous_item:
                        buy_price = float(item.replace('\'', ''))

            # CSV title, type, num_bids, cur_bid, buy_price, end_date, link
            if (type(num_bids) is int) and buy_price: # Auction & direct
                auction = [article_title, 'hybrid', num_bids, cur_bid, buy_price, end_date, article_link]
            elif buy_price: # Only direct
                auction = [article_title, 'direct', None, None, buy_price, end_date, article_link]
            else:  # Only auction
                auction = [article_title, 'auction', num_bids, cur_bid, None, end_date, article_link]

            auction_list.append(auction)

        return auction_list


if __name__ == "__main__":
    rs = RicardoScraper('https://Ricardo.ch')
    rs.get_products()
