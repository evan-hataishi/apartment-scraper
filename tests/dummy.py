from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import re

import sys
sys.path.append("../src")
import apartment as ap
import scraper as sc

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

# page_source = open('esplenade.html', 'r').read()

# s = BeautifulSoup(page_source, features="lxml")

# cards = split_apartment_html(s)
#
# print("Type\tSQFT\tPrice\t\tAvail.\tFloorplan")
#
# for card in cards:
#     type = parse_type(card)
#     sqft = parse_sqft(card)
#     price = parse_price(card)
#     availability = parse_availability(card)
#     floorplan = parse_floorplan(card)
#     print("%s\t%s\t%s\t\t%s\t%s\t" % (type, sqft, price, availability, floorplan))

# http://toddhayton.com/2015/02/03/scraping-with-python-selenium-and-phantomjs/
# http://thiagomarzagao.com/2013/11/12/webscraping-with-selenium-part-1/

s = sc.TheStandard(url='the_standard.html')
s.scrape()
# s.fetch_html()
# s.print_html()
