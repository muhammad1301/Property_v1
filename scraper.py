import json
import requests
from bs4 import BeautifulSoup
from driver import *
import time
import csv
import os

Header = ["urls"]

def open_links():
    csv_file_path = 'property2.csv'

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
    fp = 'property2.csv'
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
        self.scrape()

    def search(self):
        # city_nm = input("Enter City Name:")
        time.sleep(25)
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
        csv_file_path = 'property2.csv'
        with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader, None)

            for row in csv_reader:
                if row:
                    link = row[0]
                    print(f'Processing link: {link}')
                    res= requests.get(link)
                    html_con = res.text
                    self.content(html_con,link)

    def content(self,html_con2,link):
        soup = BeautifulSoup(html_con2, features = 'lxml')
        title = soup.find('h1').text
        bedrooms = soup.find(
            lambda tag: tag.name == "span" and tag.text == "Bedrooms:").find_next_sibling().text.strip()
        bathrooms = soup.find(
            lambda tag: tag.name == "span" and tag.text == "Bathrooms:").find_next_sibling().text.strip()
        Price = soup.find("div", class_="p24_price").text
        Listing_Number = soup.find('div', class_="col-6 p24_propertyOverviewKey").find_next_sibling().text.strip()
        try:
            Garages = soup.find(
                lambda tag: tag.name == "span" and tag.text == "Garages:").find_next_sibling().text.strip()
        except:
            Garages = "0"
        try:
            Parking = soup.find(
                lambda tag: tag.name == "span" and tag.text == "Parking:").find_next_sibling().text.strip()
        except:
            Parking = "0"
        feature_elements = soup.select('[class*="p24_propertyOverviewKey"]')
        features = {
            element.text.strip(): element.find_next_sibling().text.strip() for element in feature_elements
        }

        data = {
            "Url":link,
            "Title": title,
            "Price":Price,
            "Bedrooms":bedrooms,
            "Bathroom":bathrooms,
            "Garages":Garages,
            "Parking":Parking,
            **features,
        }
        file_name = 'property.json'
        with open(file_name, 'a') as json_file:
            json.dump(data, json_file, indent=4)
