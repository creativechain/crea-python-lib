.PHONY: clean-pyc clean-build docs

TAG := $(shell git describe master --abbrev=0)
TAGCREA := $(shell git describe master --abbrev=0 | tr "." "-")

#
clean: clean-build clean-pyc

clean-build:
	rm -fr build/ dist/ *.egg-info .eggs/ .tox/ __pycache__/ .cache/ .coverage htmlcov src
	rm -rf contrib/tmp/creapy/

clean-pyc:
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 creapyapi/ creapybase/ creapy/

test:
	python3 setup.py test

build:
	python3 setup.py build

install: build
	python3 setup.py install

install-user: build
	python3 setup.py install --user

git:
	git push --all
	git push --tags

check:
	python3 setup.py check

dist:
	python3 setup.py sdist upload -r pypi
	python3 setup.py bdist_wheel upload

release: clean check dist crea-changelog git

crea-changelog:
	git show -s --pretty=format: $(TAG) | tail -n +4 | creapy post --file "-" --author chainsquad --permlink "crea-lib-changelog-$(TAGCREA)" --category crea --title "[Changelog] crea-lib $(TAG)" --tags crea-lib changelog
