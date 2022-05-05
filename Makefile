init::
	python -m pip install --upgrade pip
	pip install -r requirements.txt

black:
	black .

black-check:
	black --check .

flake8:
	flake8 .

lint: black-check flake8

run::
	uvicorn main:app --reload
