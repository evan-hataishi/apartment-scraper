from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.firefox.options import Options
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

    def parse_apartment_html(self, apartment_html):
        data = {}
        data['type'] = self.parse_type(apartment_html)
        data['sqft'] = self.parse_sqft(apartment_html)
        data['price'] = self.parse_price(apartment_html)
        data['availability'] = self.parse_availability(apartment_html)
        data['floorplan'] = self.parse_floorplan(apartment_html)
        return ap.Apartment(**data)

    def parse_type(self, apartment_html):
        raise NotImplementedError("Must override parse_type")

    def parse_sqft(self, apartment_html):
        raise NotImplementedError("Must override parse_sqft")

    def parse_price(self, apartment_html):
        raise NotImplementedError("Must override parse_price")

    def parse_availability(self, apartment_html):
        raise NotImplementedError("Must override parse_availability")

    def parse_floorplan(self, apartment_html):
        raise NotImplementedError("Must override parse_floorplan")

class TheStandard(Scraper):

    url = "https://thestandardsanjose.securecafe.com/onlineleasing/the-standard-ca/floorplans"

    def __init__(self, **kwargs):
        kwargs['url'] = kwargs.get('url', self.url)
        super().__init__(**kwargs)

    def split_apartment_html(self):
        return self.soup.find_all("div", "fp-card")

    def parse_type(self, apartment_html):
        type = apartment_html.find("span", "fp-type").string.strip()
        if type == "Studio":
            return (0, 1)
        s = type.split()
        return (int(s[0]), int(s[3]))

    def parse_sqft(self, apartment_html):
        return apartment_html.find_all("span")[2].text.split()[0].strip()

    def parse_price(self, apartment_html):
        div = apartment_html.find("div", "fp-price")
        if len(div) < 2:
            return 0
        return div.find_all("span")[1].string.strip()

    def parse_availability(self, apartment_html):
        div = apartment_html.find("div", "fp-availability")
        text = div.text.strip()
        if len(text) == 0:
            return 0
        return int(text.split()[0])

    def parse_floorplan(self, apartment_html):
        return apartment_html.find("h2", "fp-description").string.strip()
