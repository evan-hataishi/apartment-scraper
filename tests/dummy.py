from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options

# options = Options()
# options.headless = True
#
# driver = webdriver.Firefox(options=options, executable_path='./geckodriver')
# url = "https://thestandardsanjose.securecafe.com/onlineleasing/the-standard-ca/floorplans"
#
# driver.get(url)
# page_source = driver.page_source
# driver.quit()

def parse_type(s):
    if s == "Studio":
        return s.lower()
    a = s.split()
    return a[0] + "b" + a[3] + "b"

def parse_price(div):
    # print(div.span)
    # print(len(div))
    if len(div) < 2:
        return 0
    return div.find_all("span")[1].string.strip()

def parse_availability(div):
    text = div.text.strip()
    if len(text) == 0:
        return 0
    return text.split()[0]

page_source = open('the_standard.html', 'r').read()

s = BeautifulSoup(page_source, features="lxml")

cards = s.find_all("div", "fp-card")

print("Type\tSQFT\tPrice\t\tAvail.\tFloorplan")

for card in cards:
    type = parse_type(card.find("span", "fp-type").string.strip())
    sqft = card.find_all("span")[2].text.split()[0].strip()
    price = parse_price(card.find("div", "fp-price"))
    available = parse_availability(card.find("div", "fp-availability"))
    floorplan = card.find("h2", "fp-description").string.strip()
    print("%s\t%s\t%s\t\t%s\t%s\t" % (type, sqft, price, available, floorplan))

# print(s)
# p_element = driver.find_element_by_id(id_='intro-text')
# print(p_element.text)

# http://toddhayton.com/2015/02/03/scraping-with-python-selenium-and-phantomjs/
# http://thiagomarzagao.com/2013/11/12/webscraping-with-selenium-part-1/
