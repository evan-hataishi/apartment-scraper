# apartment-scraper

Crappy web scraper to (attempt to) track prices of specific apartments over time. I found this [link](https://elitedatascience.com/python-web-scraping-libraries) useful for getting started.

## Dependencies

This project is fully developed in python3 and relies on some of the modules specified in the requirements.txt.

```bash
make install OR pip3 install -r requirements.txt
```

Selenium is needed to process the sites that use javascript, and we specifically use firefox. The [geckodriver](https://github.com/mozilla/geckodriver/releases) executable will need to be installed on your system and made available on your PATH.
