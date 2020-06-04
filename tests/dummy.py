from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import re

# options = Options()
# options.headless = True
#
# driver = webdriver.Firefox(options=options, executable_path='../src/geckodriver')
# url = "https://www.essexapartmenthomes.com/apartments/the-esplanade/floor-plans-and-pricing"
#
# driver.get(url)
# page_source = driver.page_source
# driver.quit()
#
# print(page_source)

# Super useful link: https://stackoverflow.com/questions/22726860/beautifulsoup-webscraping-find-all-finding-exact-match

def split_apartment_html(html):
    return html.find_all("div", "floor-plan-card")

def parse_type(html):
    type_sqft = html.find("p", "floor-plan-card__content__size").text.split("Bath")
    type = type_sqft[0].strip().split()
    beds = 0 if type[0] == "Studio" else type[0]
    baths = type[-1]
    return (int(beds), int(baths))

def parse_sqft(html):
    type_sqft = html.find("p", "floor-plan-card__content__size").text.split("Bath")
    sqft = type_sqft[1].strip().split()[0]
    return sqft

def parse_price(html):
    price = html.find("p", "floor-plan-card__content__price").text.strip()
    if "Contact" in price:
        return -1
    return price.split()[-1]

def parse_availability(html):
    button = html.find("button", "button-primary")
    if not button:
        return -1
    return button.span.text.strip().split()[0][1:-1]

def parse_floorplan(html):
    fp = html.find("p", "floor-plan-card__content__layout")
    return fp.text.strip().split()[0]

page_source = open('esplenade.html', 'r').read()

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
