# -*- coding: utf-8 -*-

import logging

from traits.api import HasTraits, Instance, Str, List, Dict

from Cheetah.Template import Template as CheetahTemplate

from dictionary_service.api import SQLDatabase

from library_service.library_store import LibraryStore

l = logging.getLogger(__name__)


class Template(CheetahTemplate):
    
    def __init__(self, template_string, **kwargs):
        CheetahTemplate.__init__(self, template_string, searchList=[kwargs])
        
        
class Searcher(HasTraits):
    
    sql_database = Instance(SQLDatabase)
    
    library_store = Instance(LibraryStore)
    
    _recommended_read_html = Str
    
    _url_html = Str
    
    _my_document_html = Str
    
    _shared_document_html = Str
    
    _latest_news_html = Str
    
    _additions_html = Str
    
    _my_library_html = Str
    
    _shared_library_html = Str
    
    _news_urls = List
    
    _additions_urls = List
    
    def search(self, user_id, data):
        return ''
    
    def get_search_page(self, user_id):
        page = ''.join([
                       self._get_todays_recommended_read(),
                       str(self._get_my_library(user_id)),
                       self._get_shared_library(),
                       str(self._get_latest_news()),
                       str(self._get_recent_additions()),
                       self._get_search_query_page()])
        
        return u'<div class="search_page">' + page + u'</div>'
    
    def _get_todays_recommended_read(self):
#        daily_url='www.iu.edu.sa/edu/syukbah/qis2_1.htm'
#        daily_url = 'ejtaal.net/islam/madeenah-arabic/processed_qis2_all.htm'
        daily_url = 'www.arabicreader.net/documents/qisas/qisas_modified.htm'
        url_html = Template(self._url_html,
                                daily_url=daily_url,
                                description=u'قصص الأنبياء').respond()
        return Template(self._recommended_read_html, daily_url_html=url_html).respond()
    
    def __news_urls_default(self):
        return [
#                ('news.bbc.co.uk/hi/arabic/news/', 'The BBC news localised into Arabic'),
#                ('www.alarabiya.net', 'A Saudi-owned news service'), 
#                ('www.aljazeera.net', 'The original, Qatar-based, arabic news service'),
                ('www.asharqalawsat.com', 'A London-based newspaper'),
                ]
        
    def __additions_urls_default(self):
        return [
                ('arabic.islamicweb.com/books/', 'A collection of some islamic books'),
                ('www.ghazali.org/ihya/ihya.htm', 'The famous Revival of The Religious Sciences'),
                ('www.islampedia.com', 'A nice collection of articles on Islam'),
                ('www.iu.edu.sa/edu/thanawi/2/NahwSarf/index.htm','Arabic grammar lessons'),
                ('www.iu.edu.sa/edu/thanawi/3/NahwSarf/index.htm','Arabic grammar lessons (part 2)'),
                ('www.reefnet.gov.sy/education/kafaf/index.html','Other arabic grammar lessons'),
                ('al-islam.com/arb/', ''),
                ('www.arabicreader.net/documents/qisas/qisas_modified.htm', 'A local copy of Qisas'),
                ]
        
    
    def _get_latest_news(self):
        news_html = ''
        for news_url, description in self._news_urls:
            news_html += Template(self._url_html,
                                daily_url=news_url,
                                description=description).respond()
        return Template(self._latest_news_html, news_html=news_html).respond()
    
    def _get_my_library(self, user_id):
        try:
            my_documents_html = ''
            for title in self._my_library_titles(user_id):
                my_documents_html += Template(self._my_document_html,
                                    user_id=user_id,
                                    title=title).respond()
            return Template(self._my_library_html,
                            my_documents_html=my_documents_html).respond()
        except Exception as ex:
            l.exception("getting My Library html: %s", ex)
            return 'Sorry: There was an error retrieving your library. Please contact the administrator.'
    
    def _get_shared_library(self):
        shared_documents_html = ''
        for user_id, title, user_name in self._shared_library_titles():
            shared_documents_html += Template(self._shared_document_html,
                                user_id=user_id,
                                user_name=user_name,
                                title=title).respond()
        return Template(self._shared_library_html,
                        shared_documents_html=shared_documents_html).respond()
    
    def _get_recent_additions(self):
        additions_html = ''
        for addition_url, description in self._additions_urls:
            additions_html += Template(self._url_html,
                                daily_url=addition_url,
                                description=description).respond()
        return Template(self._additions_html, additions_html=additions_html).respond()
    
    def _my_library_titles(self, user_id):
        return self.library_store.get_available_titles(user_id)
    
    def _shared_library_titles(self):
        return self.library_store.get_shared_titles()
    
    def _get_search_query_page(self):
        return ''
    
    def __recommended_read_html_default(self):
        return \
"""
<div>
    <h3>Today's Recommended Read
    </h3>
    <div>
        $daily_url_html
    </div>
</div>
"""
        
    def __url_html_default(self):
        return \
"""
<div>
<span class="about_link" onclick="mode.goto_url('$daily_url')">$daily_url</span>
</div>
<div>
$description
</div>
"""

    def __my_document_html_default(self):
        return \
"""
<div>
<span class="about_link" onclick="mode.goto_library_document($user_id, '$title')">$title</span>
<span class="share_link" onclick="library.share_library_file($user_id, '$title')">(share)</span>
<span class="delete_link" onclick="library.delete_library_file($user_id, '$title')">(delete)</span>
</div>
"""

    def __shared_document_html_default(self):
        return \
"""
<div>
<span class="about_link" onclick="mode.goto_library_document($user_id, '$title')">$title (shared by $user_name)</span>
</div>
"""

    def __latest_news_html_default(self):
        return \
"""
<div>
    <h3>Latest News
    </h3>
    <div>
        $news_html
    </div>
</div>
"""

    def __additions_html_default(self):
        return \
"""
<div>
    <h3>Recent Additions
    </h3>
    <div>
        $additions_html
    </div>
</div>
"""

    def __my_library_html_default(self):
        return \
"""
<div>
    <h3>My Library
    </h3>
    <div>
        $my_documents_html
    </div>
</div>
"""

    def __shared_library_html_default(self):
        return \
"""
<div>
    <h3>Shared Library
    </h3>
    <div>
        $shared_documents_html
    </div>
</div>
"""
   