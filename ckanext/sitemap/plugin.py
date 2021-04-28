import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from flask import Blueprint
import ckanext.sitemap.views as views

class SitemapPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IBlueprint)

    def get_blueprint(self):
        plugin = Blueprint(u'sitemap', self.__module__)
        plugin.add_url_rule(u'/sitemap.xml', view_func=views.view)

        return [plugin]
