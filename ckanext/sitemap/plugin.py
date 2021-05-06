from flask import Blueprint
import ckan.plugins as plugins
from flask_caching import Cache
import ckanext.sitemap.views as views
import ckan.plugins.toolkit as toolkit

from ckan.common import config as c


class SitemapPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IMiddleware, inherit=True)


    def make_middleware(self, app, config):
        """
        Set up page caching for the sitemap.

        Caching needs access to the app and the view function or where the
        rule is added. CKAN loads the blueprints before the middleware, so
        it's impossible to use a normal blueprint function.

        https://docs.ckan.org/en/2.9/extensions/plugin-interfaces.html#ckan.plugins.interfaces.IMiddleware.make_middleware
        """
        # Use a different redis DB than CKAN, incase it needs to be cleared
        redis_url, db = c.get('ckan.redis.url').rsplit('/', 1)
        cache_redis_url = f'{redis_url}/{int(db) + 1}'

        self.cache = Cache(config={'CACHE_TYPE': 'RedisCache', 'CACHE_REDIS_URL': cache_redis_url})
        self.cache.init_app(app)
        cached_view = self.cache.cached(timeout=3600*24)(views.view)
        bp = Blueprint(u'sitemap', self.__module__)
        bp.add_url_rule(u'/sitemap.xml', view_func=cached_view)
        app.register_extension_blueprint(bp)

        return app

