# -*- coding: utf-8 -*-

import ar_logging; ar_logging.add_std_out()
import logging
import unittest
import simplejson

from sarf_service.test.test_words import *

from bs4 import BeautifulSoup
from proxy_service.url_mangler_soup import URLMangler


class TestURLManglerSoup(unittest.TestCase):
    
    def setUp(self):
        self.url_mangler = URLMangler()
        
    def test_get_site_address(self):
        url = 'http://mysite.com/this/is/a/test.html'
        site_address = self.url_mangler.site_address(url)
        self.assertEquals(site_address, 'http://mysite.com')
        url = 'http://mysite.com'
        site_address = self.url_mangler.site_address(url)
        self.assertEquals(site_address, 'http://mysite.com')
        
    def test_get_directory(self):
        url = 'http://mysite.com/this/is/a/test.html'
        dir = self.url_mangler._get_directory(url)
        self.assertEquals(dir, 'http://mysite.com/this/is/a/')
        url = 'http://mysite.com/this/is/a/'
        dir = self.url_mangler._get_directory(url)
        self.assertEquals(dir, 'http://mysite.com/this/is/a/')
        url = 'http://www.asharqalawsat.com/'
        dir = self.url_mangler._get_directory(url)
        self.assertEquals(dir, 'http://www.asharqalawsat.com/')
        
    def test_get_absolute_url(self):
        base_url = 'http://mysite.com'
        url = '/01common/pix/Asharq-alawsat-logo.jpg'
        remote_url = self.url_mangler._get_absolute_url(url, base_url)
        self.assertEquals(remote_url,
                          'http://mysite.com/01common/pix/Asharq-alawsat-logo.jpg')
        url = 'pix/Asharq-alawsat-logo.jpg'
        remote_url = self.url_mangler._get_absolute_url(url, base_url)
        self.assertEquals(remote_url,
                          'http://mysite.com/pix/Asharq-alawsat-logo.jpg')
        
        base_url = 'http://mysite.com/test/dir'
        url = '/01common/pix/Asharq-alawsat-logo.jpg'
        remote_url = self.url_mangler._get_absolute_url(url, base_url)
        self.assertEquals(remote_url,
                          'http://mysite.com/01common/pix/Asharq-alawsat-logo.jpg')
        url = 'pix/Asharq-alawsat-logo.jpg'
        remote_url = self.url_mangler._get_absolute_url(url, base_url)
        self.assertEquals(remote_url,
                          'http://mysite.com/test/dir/pix/Asharq-alawsat-logo.jpg')
        
        url = '2008/05/01/images/f_media1.468989.jpg'
        remote_url = self.url_mangler._get_absolute_url(url, base_url)
        self.assertEquals(remote_url,
                          'http://mysite.com/test/dir/2008/05/01/images/f_media1.468989.jpg')
        
    def test_get_remote_url_with_dots(self):
        base_url = 'http://mysite.com/images/test'
        url = '../01common/abc.html'
        remote_url = self.url_mangler._get_absolute_url(url, base_url)
        self.assertEquals(remote_url,
                          'http://mysite.com/images/01common/abc.html')
        
    def test_route_through_proxy(self):
        url = 'http://mysite.com/this/is/a/test.html'
        new_url = self.url_mangler._route_through_proxy(url)
        self.assertEquals(new_url, '/services/proxy/geturl/mysite.com/this/is/a/test.html')
        
    def test_replace_relative_links(self):
        html = """
        <table><tr>
        <td width="230"><a href='magazine.asp?magid=30'>
        <IMG border='0' src='/magazines/30.jpg' width='135' ></a></td>

        <td valign="top" width="135"><a href='magazine.asp?magid=35'>
        <img border='0' src='/magazines/35.jpg' width='135' ></a></td>
        <!--supplement ends-->
        </tr></table>
        """
        base_url = 'http://mysite.com/'
        new_html = self.url_mangler.replace_relative_links(html, base_url)
        