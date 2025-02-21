

all: clean build pathly

pathly:
	sudo cp dist/aptlyctl /usr/bin/

build:
	pyinstaller --onefile aptlyctl.py


clean:
	sudo rm -rf dist/ build/ aptlyctl.spec

