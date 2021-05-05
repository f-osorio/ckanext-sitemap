"""
Tests for plugin.py.

Tests are written using the pytest library (https://docs.pytest.org), and you
should read the testing guidelines in the CKAN docs:
https://docs.ckan.org/en/2.9/contributing/testing.html

To write tests for your extension you should install the pytest-ckan package:

    pip install pytest-ckan

This will allow you to use CKAN specific fixtures on your tests.

For instance, if your test involves database access you can use `clean_db` to
reset the database:

    import pytest

    from ckan.tests import factories

    @pytest.mark.usefixtures("clean_db")
    def test_some_action():

        dataset = factories.Dataset()

        # ...

For functional tests that involve requests to the application, you can use the
`app` fixture:

    from ckan.plugins import toolkit

    def test_some_endpoint(app):

        url = toolkit.url_for('myblueprint.some_endpoint')

        response = app.get(url)

        assert response.status_code == 200


To temporary patch the CKAN configuration for the duration of a test you can use:

    import pytest

    @pytest.mark.ckan_config("ckanext.myext.some_key", "some_value")
    def test_some_action():
        pass
"""
import logging
import pytest
import json
from io import StringIO
from lxml import etree
import datetime
import sqlalchemy.orm as orm

from ckan.common import config
from ckan.plugins.toolkit import url_for
from ckan.logic.auth.get import package_show

import ckan.model as model
import ckan.lib.create_test_data as ctd
import ckanext.datastore.backend.postgres as db
from ckanext.datastore.tests.helpers import set_url_type

from ckan.tests import helpers, factories

import ckanext.sitemap.tests.testdata as testdata
import ckanext.sitemap.plugin as plugin

log = logging.getLogger(__file__)

siteschema = etree.XMLSchema(etree.XML(str.encode(testdata.sitemap)))


class TestSiteMap:
    sysadmin_user = None
    normal_user = None

    @pytest.fixture(autouse=True)
    def initial_data(self, clean_db, clean_index, test_request_context, app):
        ctd.CreateTestData.create()
        self.sysadmin_user = model.User.get("testsysadmin")
        self.normal_user = model.User.get("annafan")
        engine = db.get_write_engine()
        self.Session = orm.scoped_session(orm.sessionmaker(bind=engine))
        with test_request_context():
            set_url_type(
                model.Package.get("annakarenina").resources, self.sysadmin_user
            )
        url = url_for('sitemap.view')
        self.cont = app.get(url)


    @pytest.mark.usefixtures("with_plugins")
    def test_validity(self):
        siteschema.assertValid(etree.XML(str.encode(self.cont.body)).getroottree())
        assert(siteschema.validate(etree.XML(str.encode(self.cont.body))))


    @pytest.mark.usefixtures("with_plugins")
    def test_packages(self):
        tree = etree.XML(str.encode(self.cont.body)).getroottree()
        pkg = model.Package.get("annakarenina")
        assert len(model.Package.get("annakarenina").resources) == 2
        assert "annakarenina" in pkg.name
        urli = config.get('ckan.site_url') + url_for('dataset.read', id = pkg.name)
        assert(tree.getroot()[0][0].text == urli)
        # Needs to be created today as test data is too
        pkgdate = pkg.metadata_modified.strftime('%Y-%m-%d')
        assert(tree.getroot()[0][1].text == pkgdate)


    @pytest.mark.usefixtures("with_plugins")
    def test_zcache(self, app):
        url = url_for('sitemap.view')
        cont1 = app.get(url)
        cont2 = app.get(url)
        assert(cont1.body == cont2.body)

        dataset = helpers.call_action(
            "package_patch", id="annakarenina", name="fookarenina"
        )
        assert('fookarenina' in dataset['name'])
        response = app.get(url)
        response_headers = dict(response.headers)
        assert(cont1.body == response.body)


