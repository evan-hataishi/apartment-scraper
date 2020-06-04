from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
import re
import apartment as ap

GECKO_PATH = '/home/evan/Documents/git/apartment-scraper/src/geckodriver'

class Scraper():

    def __init__(self, **kwargs):
        self.url = kwargs['url']
        self.html = None
        self.apartments = None

    def __str__(self):
        header = ap.Apartment.get_print_header()
        rows = "\n".join([str(a) for a in self.apartments])
        return "URL: " + self.url + "\n" + header + "\n" + rows

    def scrape(self):
        self.fetch_html()
        self.parse_html()
        print(self)

    def fetch_html(self, headless=True):
        if ".html" in self.url:
            self.html = Scraper.fetch_html_from_file(self.url)
        else:
            self.html = Scraper.fetch_html_from_url(self.url, headless)
        self.soup = BeautifulSoup(self.html, features="lxml")

    def fetch_html_from_file(file_name):
        with open(file_name, 'r') as f:
            return f.read()

    # TODO - error handling
    def fetch_html_from_url(url, headless):
        options = Options()
        options.headless = headless
        driver = webdriver.Firefox(options=options, executable_path=GECKO_PATH)
        driver.get(url)
        html = driver.page_source
        driver.quit()
        return html

    # Use abstract annotation using abc?
    # https://stackoverflow.com/questions/25062114/calling-child-class-method-from-parent-class-file-in-python
    def parse_html(self):
        cards = self.split_apartment_html()
        self.apartments = [self.parse_apartment_html(x) for x in cards]

    def split_apartment_html(self):
        raise NotImplementedError("Must override split_apartment_html")

    def parse_apartment_html(self, html):
        data = {}
        data['type'] = self.parse_type(html)
        data['sqft'] = self.parse_sqft(html)
        data['price'] = self.parse_price(html)
        data['availability'] = self.parse_availability(html)
        data['floorplan'] = self.parse_floorplan(html)
        return ap.Apartment(**data)

    def parse_type(self, html):
        raise NotImplementedError("Must override parse_type")

    def parse_sqft(self, html):
        raise NotImplementedError("Must override parse_sqft")

    def parse_price(self, html):
        raise NotImplementedError("Must override parse_price")

    def parse_availability(self, html):
        raise NotImplementedError("Must override parse_availability")

    def parse_floorplan(self, html):
        raise NotImplementedError("Must override parse_floorplan")

class TheStandard(Scraper):

    url = "https://thestandardsanjose.securecafe.com/onlineleasing/the-standard-ca/floorplans"

    def __init__(self, **kwargs):
        kwargs['url'] = kwargs.get('url', self.url)
        super().__init__(**kwargs)

    def split_apartment_html(self):
        return self.soup.find_all("div", "fp-card")

    def parse_type(self, html):
        type = html.find("span", "fp-type").string.strip()
        if type == "Studio":
            return (0, 1)
        s = type.split()
        return (int(s[0]), int(s[3]))

    def parse_sqft(self, html):
        return html.find_all("span")[2].text.split()[0].strip()

    def parse_price(self, html):
        div = html.find("div", "fp-price")
        if len(div) < 2:
            return -1
        return div.find_all("span")[1].string.strip()

    def parse_availability(self, html):
        div = html.find("div", "fp-availability")
        text = div.text.strip()
        if len(text) == 0:
            return 0
        return int(text.split()[0])

    def parse_floorplan(self, html):
        return html.find("h2", "fp-description").string.strip()

class CanneryPark(Scraper):

    url = "https://www.canneryparkbywindsor.com/floorplans"

    def __init__(self, **kwargs):
        kwargs['url'] = kwargs.get('url', self.url)
        super().__init__(**kwargs)

    def split_apartment_html(self):
        sections = self.soup.find_all(lambda tag: tag.name == 'div' and tag.get('class') == ['card'])
        cards = []
        for s in sections:
            cards += s.find_all("div", "row")
        return cards

    def parse_type(self, html):
        match = re.compile('Floorplan[0-9]{1,2}Beds')
        beds = html.find('span', {'data-selenium-id': match}).text.split()[0]
        if beds == 'Studio':
            beds = 0
        match = re.compile('Floorplan[0-9]{1,2}Baths')
        baths = html.find('span', {'data-selenium-id': match}).text.split()[0]
        return (int(beds), int(baths))

    def parse_sqft(self, html):
        match = re.compile('Floorplan[0-9]{1,2}SqFt')
        sqft = html.find('span', {'data-selenium-id': match})
        return sqft.text.strip().split()[0]

    def parse_price(self, html):
        match = re.compile('Floorplan[0-9]{1,2}Rent')
        price = html.find('span', {'data-selenium-id': match})
        if price.string:
            return -1
        return price.text.strip().split()[0][:-2]

    def parse_availability(self, html):
        match = re.compile('Floorplan[0-9]{1,2} Availability')
        available = html.find('span', {'data-selenium-id': match})
        return int(available.text.strip().split()[0])

    def parse_floorplan(self, html):
        match = re.compile('Floorplan[0-9]{1,2}Name')
        type = html.find('span', {'data-selenium-id': match})
        return type.text.strip()

class Esplenade(Scraper):

    url = "https://www.essexapartmenthomes.com/apartments/the-esplanade/floor-plans-and-pricing"

    def __init__(self, **kwargs):
        kwargs['url'] = kwargs.get('url', self.url)
        super().__init__(**kwargs)

    def split_apartment_html(self):
        return self.soup.find_all("div", "floor-plan-card")

    def parse_type(self, html):
        type_sqft = html.find("p", "floor-plan-card__content__size").text.split("Bath")
        type = type_sqft[0].strip().split()
        beds = 0 if type[0] == "Studio" else type[0]
        baths = type[-1]
        return (int(beds), int(baths))

    def parse_sqft(self, html):
        type_sqft = html.find("p", "floor-plan-card__content__size").text.split("Bath")
        sqft = type_sqft[1].strip().split()[0]
        return sqft

    def parse_price(self, html):
        price = html.find("p", "floor-plan-card__content__price").text.strip()
        if "Contact" in price:
            return -1
        return price.split()[-1]

    def parse_availability(self, html):
        button = html.find("button", "button-primary")
        if not button:
            return -1
        return button.span.text.strip().split()[0][1:-1]

    def parse_floorplan(self, html):
        fp = html.find("p", "floor-plan-card__content__layout")
        return fp.text.strip().split()[0]
