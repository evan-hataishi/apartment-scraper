
default: test

install:
	pip3 install -r requirements.txt

test:
	cd tests; python3 -u dummy.py
