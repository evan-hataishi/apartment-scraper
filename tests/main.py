# Stupid workaround to import from parent directory
import sys
sys.path.append("../src")
import apartment as ap
import scraper as sc


def main():
    the_standard = sc.TheStandard(url='the_standard.html')
    the_standard = sc.TheStandard()
    the_standard.scrape()


if __name__ == '__main__':
    main()
