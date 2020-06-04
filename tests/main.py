# Stupid workaround to import from parent directory
import sys
sys.path.append("../src")
import apartment as ap
import scraper as sc

USE_OLD = False

def do_stuff(apartments):
    for a in apartments:
        a.scrape()

def main():
    old = [sc.TheStandard(url='the_standard.html'), sc.CanneryPark(url='cannery_park.html'), sc.Esplenade(url='esplenade.html')]
    updated = [sc.TheStandard(), sc.CanneryPark(), sc.Esplenade()]

    if USE_OLD:
        do_stuff(old)
    else:
        do_stuff(updated)

if __name__ == '__main__':
    main()
