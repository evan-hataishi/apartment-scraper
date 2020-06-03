from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import re

# options = Options()
# options.headless = True
#
# driver = webdriver.Firefox(options=options, executable_path='../src/geckodriver')
# url = "https://www.canneryparkbywindsor.com/floorplans"
#
# driver.get(url)
# page_source = driver.page_source
# driver.quit()
#
# print(page_source)

# Super useful link: https://stackoverflow.com/questions/22726860/beautifulsoup-webscraping-find-all-finding-exact-match

def split_apartment_html(html):
    sections = html.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['card'])
    cards = []
    for s in sections:
        cards += s.find_all("div", "row")
    return cards

def parse_type(html):
    match = re.compile('Floorplan[0-9]{1,2}Beds')
    beds = html.find('span', {'data-selenium-id': match}).text.split()[0]
    if beds == 'Studio':
        beds = 0
    match = re.compile('Floorplan[0-9]{1,2}Baths')
    baths = html.find('span', {'data-selenium-id': match}).text.split()[0]
    return (int(beds), int(baths))

def parse_sqft(html):
    match = re.compile('Floorplan[0-9]{1,2}SqFt')
    sqft = html.find('span', {'data-selenium-id': match})
    return sqft.text.strip().split()[0]

def parse_price(html):
    match = re.compile('Floorplan[0-9]{1,2}Rent')
    price = html.find('span', {'data-selenium-id': match})
    if price.string:
        return -1
    return price.text.strip().split()[0][:-2]

def parse_availability(html):
    match = re.compile('Floorplan[0-9]{1,2} Availability')
    available = html.find('span', {'data-selenium-id': match})
    return int(available.text.strip().split()[0])

def parse_floorplan(html):
    match = re.compile('Floorplan[0-9]{1,2}Name')
    type = html.find('span', {'data-selenium-id': match})
    return type.text.strip()

page_source = open('cannery_park.html', 'r').read()

s = BeautifulSoup(page_source, features="lxml")

cards = split_apartment_html(s)
#
# print("Type\tSQFT\tPrice\t\tAvail.\tFloorplan")
#
for card in cards:
    type = parse_type(card)
    sqft = parse_sqft(card)
    price = parse_price(card)
    availability = parse_availability(card)
    floorplan = parse_floorplan(card)
    print("%s\t%s\t%s\t\t%s\t%s\t" % (type, sqft, price, availability, floorplan))

# http://toddhayton.com/2015/02/03/scraping-with-python-selenium-and-phantomjs/
# http://thiagomarzagao.com/2013/11/12/webscraping-with-selenium-part-1/
