
import logging

from traits.api import Instance

from server.api import Handler
from dictionary_service.api import SQLDatabase

from library_service.library_store import LibraryStore
from library_service.searcher import Searcher

l = logging.getLogger(__name__)


class LibraryHandler(Handler):
    
    library_store = Instance(LibraryStore)
    
    searcher = Instance(Searcher)
    
    sql_database = Instance(SQLDatabase)
    
    def _url_lookup_default(self):
        lookup = {
                  'upload': self._upload,
                  'dir': self._dir,
                  'download': self._download,
                  'search_page': self._search_page,
                  'do_search': self._search,
                  'documents': self._documents,
                  'delete': self._delete,
                  'share': self._share,
        }
        return lookup
    
    def _upload(self, data, session, **kwargs):
        if not session.authenticated:
            raise Exception('You must be authenticated to upload to your library')
        title = kwargs['upload_title']
        upload_field = kwargs['upload_file']
        if not session.authenticated:
            raise Exception('You must be authenticated to upload files')
        
        self.library_store.save_file(session.user_id, title, upload_field.file)
        
    def _dir(self, data, session):
        if not session.authenticated:
            raise Exception('You must be authenticated to see your library')
        data = str(data)
        return self.library_store.get_available_titles(session.user_id)
    
    def _download(self, data, session):
        if not session.authenticated:
            raise Exception('You must be authenticated to download from your library')
        data = str(data)
        file = self.library_store.get_file(session.user_id, data)
        return file.read()
    
    def _delete(self, data, session):
        if not session.authenticated:
            raise Exception('You must be authenticated to delete from your library')
        return self.library_store.delete(session.user_id, data)
    
    def _share(self, data, session):
        if not session.authenticated:
            raise Exception('You must be authenticated to share from your library')
        return self.library_store.share(session.user_id, data)
    
    def _search(self, data, session):
        return self.searcher.search(session.user_id, data)
    
    def _search_page(self, data, session):
        return self.searcher.get_search_page(session.user_id)
    
    def _documents(self, data, session):
        user_id, title, page_no = data.split('/')
        user_id = int(user_id)
        l.debug('title: %s %s', title, repr(title))
        title = title
        page_no = int(page_no)
        shared = self.library_store.get_shared(user_id, title)
        if not shared:
            if not session.authenticated:
                raise Exception('You must be authenticated to download from your library')
            if not session.user_id == user_id:
                raise Exception("You cannot download other users' documents")
        title = title.encode('utf-8')
        page_data = self.library_store.get_file_page_data(user_id, title, page_no)
        return page_data
            

