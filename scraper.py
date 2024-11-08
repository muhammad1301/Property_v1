import requests

from driver import *
import time
import csv
import os

Header = ["urls"]

def open_links():
    csv_file_path = 'property.csv'

    # Open the CSV file and read it line by line
    with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        # Skip the header row if there is one
        next(csv_reader, None)

        for row in csv_reader:
            if row:  # Check if the row is not empty
                link = row[0]  # Assuming links are in the first column
                print(f'Processing link: {link}')

def writing_csv(row):
    fp = 'property.csv'
    with open(fp, 'a', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        if os.path.getsize(fp) == 0:
            writer.writerow(Header)
        writer.writerow(row)


class Property(Selenium):

    def open_web(self):
        BASED_URL = 'https://www.property24.com/'
        self.get(BASED_URL)
        self.search()

    def search(self):
        # city_nm = input("Enter City Name:")
        time.sleep(20)
        self.wait.until(EC.presence_of_element_located((By.XPATH, '//input[@id="token-input-AutoCompleteItems"]')))
        print("starting")
        search = self.find_element(By.XPATH, '//input[@id="token-input-AutoCompleteItems"]')
        search.click()
        search.send_keys("sea point")
        time.sleep(3)
        search.send_keys(Keys.ENTER)
        self.find_element(By.XPATH, '//button[@class="btn btn-danger"]').click()
        self.crawl()
        self.scrape()

    def crawl(self):
        i = 1
        while True:
            try:
                self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="p24_regularTile '
                                                                          'js_rollover_container js_resultTileClickable'
                                                                          '   p24_tileHoverWrapper"]//span//a')))
                url = self.href(By.XPATH, f'(//div[@class="p24_regularTile js_rollover_container js_resultTileClickable   p24_tileHoverWrapper"]//span//a)[{i}]')
                print(i,url)
                i += 1
                row = [url]
                writing_csv(row)
            except NoSuchElementException:
                break
    def scrape(self):
        csv_file_path = 'property.csv'

        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader, None)

            for row in csv_reader:
                if row:
                    link = row[0]
                    print(f'Processing link: {link}')
                    res= requests.get(link)
                    html_con = res.text
                    print(html_con)