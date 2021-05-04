from lxml import etree
from flask import make_response
from ckan.common import config
from ckan.model import Session, Package
from ckan.plugins.toolkit import url_for


SITEMAP_NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
XHTML_NS = 'http://www.w3.org/1999/xhtml'


def render_sitemap():
    root = etree.Element('urlset', nsmap={None: SITEMAP_NS, 'xhtml': XHTML_NS})
    pkgs = Session.query(Package).filter(Package.type=='dataset').filter(Package.private!=True).\
            filter(Package.state=='active').all()
    for pkg in pkgs:
        url = etree.SubElement(root, 'url')
        loc = etree.SubElement(url, 'loc')
        pkg_url = url_for('dataset.read', id=pkg.name)
        loc.text = config.get('ckan.site_url') + pkg_url
        lastmod = etree.SubElement(url, 'lastmod')
        lastmod.text = pkg.metadata_modified.strftime('%Y-%m-%d')
    return etree.tostring(root, pretty_print=True)

def view():
    resp = make_response(render_sitemap())
    resp.headers['Content-type'] = 'text/xml'

    return resp
