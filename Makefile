init::
	python -m pip install --upgrade pip
	pip install -r requirements.txt
	npm install

black:
	black .

black-check:
	black --check .

flake8:
	flake8 .

lint: black-check flake8

stylesheets:
	npm run build:gel
	npm run build:stylesheets

run::
	uvicorn main:app --reload
