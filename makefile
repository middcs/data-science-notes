.ONESHELL: 

SHELL = /bin/zsh

PYTHON ?= env/bin/python3

stage: 
	quarto render
	$(PYTHON) scripts/create-ipynb.py

publish: 
	quarto render
	$(PYTHON) scripts/create-ipynb.py
	git add .
	git commit -m "Update"
	git push

prep:
	$(PYTHON) scripts/create-ipynb.py

preview: 
	quarto preview

clean: 
	find . -type f -name "* [0-9]*" -delete
	find . -name "* [0-9]*" -type d -exec rm -r "{}" \;
	rm -rf docs	

