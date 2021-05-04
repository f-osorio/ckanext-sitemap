[![Tests](https://github.com/f-osorio/ckanext-sitemap/workflows/Tests/badge.svg?branch=main)](https://github.com/f-osorio/ckanext-sitemap/actions)

# ckanext-sitemap

Creates an XML sitemap for CKAN. The sitemap only includes datasets, no resources.


## Requirements

Only tested with CKAN 2.9.2 and Python3.

- flask_caching

## Installation

To install ckanext-sitemap:

1. Activate your CKAN virtual environment, for example:

     . /usr/lib/ckan/default/bin/activate

2. Clone the source and install it on the virtualenv

    git clone https://github.com/f-osorio/ckanext-sitemap.git
    cd ckanext-sitemap
    pip install -e .
	pip install -r requirements.txt

3. Add `sitemap` to the `ckan.plugins` setting in your CKAN
   config file (by default the config file is located at
   `/etc/ckan/default/ckan.ini`).

4. Restart CKAN. For example if you've deployed CKAN with Apache on Ubuntu:

     sudo service apache2 reload


## Config settings

None at present

**TODO:** Document any optional config settings here. For example:

	# The minimum number of hours to wait before re-checking a resource
	# (optional, default: 24).
	ckanext.sitemap.some_setting = some_default_value


## Developer installation

To install ckanext-sitemap for development, activate your CKAN virtualenv and
do:

    git clone https://github.com/f-osorio/ckanext-sitemap.git
    cd ckanext-sitemap
    python setup.py develop
    pip install -r dev-requirements.txt


## Tests

To run the tests, do:

    pytest --ckan-ini=test.ini


## License

[AGPL](https://www.gnu.org/licenses/agpl-3.0.en.html)
