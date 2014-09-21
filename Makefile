.PHONY: install uninstall pypi

devinstall:
	pip install --editable .

uninstall:
	pip uninstall pelican_publications

pypi:
	python setup.py sdist upload
	python setup.py bdist_egg upload
	python setup.py bdist_wheel upload
