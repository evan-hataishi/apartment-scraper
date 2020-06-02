
default: main

install:
	pip3 install -r requirements.txt

test:
	cd tests; python3 -u dummy.py

main:
	cd tests; python3 -u main.py
