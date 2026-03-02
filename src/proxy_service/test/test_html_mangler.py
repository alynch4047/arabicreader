# -*- coding: utf-8 -*-

import ar_logging; ar_logging.add_std_out()
import logging
import unittest
import simplejson

from sarf_service.test.test_words import *

from bs4 import BeautifulSoup
from proxy_service.url_mangler import URLMangler
from proxy_service.hmtl_mangler import HTMLMangler


class TestHTMLMangler(unittest.TestCase):
    
    def setUp(self):
        url_mangler = URLMangler()
        self.html_mangler = HTMLMangler(url_mangler=url_mangler)
        
    def test_fixup_header_links_import(self):
        html = \
"""
<html>
<head>
<style>
    @import "/def/ghi.cc";
    @import "f.css";
</style>
<stuff/>يث
</head>
<body id='abc' onLoad="doSomething()">
<p>test</p>
</body>
</html>
"""
        html = str(html)
        new_html = self.html_mangler.fixup_header_links(html, 'http://www.abc.com/start/url/')
        self.assertEquals(new_html,
"""
<html>
<head>
<style>
    @import "http://www.abc.com/def/ghi.cc";
    @import "http://www.abc.com/start/url/f.css";
</style>
<stuff/>يث
</head>
<body id='abc' onLoad="doSomething()">
<p>test</p>
</body>
</html>
""")
        
    def test_fixup_header_links(self):
        html = \
"""
<html>
<head>
<link rel='abc' href='details.asp?def'>
<link rel='def' href='details2.asp?def' img='def'>
<style>
    @import "/def/ghi.cc";
    @import "f.css";
</style>
<stuff/>يث
</head>
<body id='abc' onLoad="doSomething()">
<p>test</p>
</body>
</html>
"""
        html = str(html)
        new_html = self.html_mangler.fixup_header_links(html, 'http://www.abc.com/start/url/')
        self.assertEquals(new_html,
"""
<html>
<head>
<link rel='abc' href='http://www.abc.com/start/url/details.asp?def'>
<link rel='def' href='http://www.abc.com/start/url/details2.asp?def' img='def'>
<style>
    @import "http://www.abc.com/def/ghi.cc";
    @import "http://www.abc.com/start/url/f.css";
</style>
<stuff/>يث
</head>
<body id='abc' onLoad="doSomething()">
<p>test</p>
</body>
</html>
""")
        
    def test_fixup_header_links_2(self):
        html = \
"""
<head>
<link rel='abc' href='details.asp?def'>
</head>
<body>
</body>
"""
        new_html = self.html_mangler.fixup_header_links(html, 'http://www.abc.com/start/url/')
        self.assertEquals(new_html,
"""
<head>
<link rel='abc' href='http://www.abc.com/start/url/details.asp?def'>
</head>
<body>
</body>
""")
        
    def test_body_on_load(self):
        html = \
"""
<html>
<body id='abc' onLoad="doSomething()">
<p>test</p>
</body>
</html>
"""
        soup = BeautifulSoup(html)
        soup.body['id']
        soup.body['onload']
        res = self.html_mangler._set_up_on_load(soup)
        body_on_load = soup.body['onload']
        self.assertEquals(body_on_load, """doSomething(); if_ar.init()""")
        html2 = \
"""
<html>
<body>
<p>test</p>
</body>
</html>
"""
        soup = BeautifulSoup(html2)
        res = self.html_mangler._set_up_on_load(soup)
        body_on_load = soup.body['onload']
        self.assertEquals(body_on_load, """if_ar.init()""")


        
