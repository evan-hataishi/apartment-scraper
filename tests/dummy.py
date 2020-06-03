from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options

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
    print(len(sections[0].find_all("div", "row")))
    cards = [s.find_all("div", "row") for s in sections]
    return cards

def parse_type(html):
    # html.find("div", "mb-2 d-flex flex-wrap")
    pass

def parse_sqft(html):
    pass

def parse_price(html):
    pass

def parse_availability(html):
    pass

def parse_floorplan(html):
    pass

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
