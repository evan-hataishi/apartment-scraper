import urllib3

http = urllib3.PoolManager()

def get_html(url):
    # page = requests.get(url)
    r = http.request('GET', url)
    print(r.text)
    # return BeautifulSoup(page.content, features="lxml")

def fetch_standard():
    url = "https://thestandardsanjose.securecafe.com/onlineleasing/the-standard-ca/floorplans"
    soup = get_html(url)
    # items = soup.find_all('script')
    # for a in items:
        # x = a.string
        # if x and len(x) > 11 and "var pageData" in x[:12]:
        #     data = x[15:-1]
        #     json.loads(data.replace(": ", "= "))
        #     print(data)

def main():
    fetch_standard()


if __name__ == '__main__':
    main()
