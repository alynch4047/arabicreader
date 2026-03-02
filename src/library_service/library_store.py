
import logging
import os
import random
import threading
import shelve
import codecs
import atexit

from traits.api import HasTraits, Str, Dict, Instance

from session_service.api import MIN_GUEST_ID, MAX_GUEST_ID
from dictionary_service.api import SQLDatabase

from server.memory import mem

l = logging.getLogger(__name__)

_lock = threading.Lock()

NUM_BYTES_IN_PAGE = 3000


class LibraryStore(HasTraits):
    
    root_path = Str
    
    sql_database = Instance(SQLDatabase)
    
    shelves = Dict # user_id -> shelf
    
    def __init__(self, **traits):
        super(LibraryStore, self).__init__(**traits)
        assert(os.path.isdir(self.root_path))
        atexit.register(self._close_shelves)
        
    def _save_shelf(self, user_id):
        l.debug('save shelf for %s', user_id)
        shelf = self._get_shelf(user_id)
        shelf.close()
        del self.shelves[user_id]
        
    def _close_shelves(self):
        for user_id, shelf in self.shelves.items():
            try:
                l.debug('close shelf for %s', user_id)
                shelf.close()
            except:
                l.exception('closing shelf for %s', user_id)
        
    def _get_shelf(self, user_id):
        if user_id in self.shelves:
            shelf = self.shelves[user_id]
        else:
            user_dir = self._make_user_dir(user_id)
            shelf_path = os.path.join(user_dir, 'titles_shelf')
            shelf = shelve.open(shelf_path)
            self.shelves[user_id] = shelf
        return shelf
    
    def save_file(self, user_id, title, input_file):
        """ Save the given file of title for the user"""
        user_dir = self._make_user_dir(user_id)
        filename = self._generate_file_name(user_dir)
        save_file_path = os.path.join(user_dir, filename)
        f = open(save_file_path, 'wb+')
        while True:
            data = input_file.read(8192)
            if not data:
                break
            f.write(data)
        f.close()
        _lock.acquire()
        try:
            shelf = self._get_shelf(user_id)
            l.debug('save file with title %s %s', title, repr(title))
            shelf[title] = [filename, False]
            self._save_shelf(user_id)
        finally:
            _lock.release()
            
    def _generate_file_name(self, user_dir):
        """ Generate a unique file name for a file name in the given directory"""
        dir = os.listdir(user_dir)
        while True:
            filename = str(random.randint(MIN_GUEST_ID, MAX_GUEST_ID))
            if filename not in dir:
                break
        return filename
    
    def get_available_titles(self, user_id):
        """ Return a list of the available titles for the given user"""
        if user_id < MIN_GUEST_ID:
            shelf = self._get_shelf(user_id)
            titles = list(shelf.keys())
            return titles
        else:
            return []
    
    def _get_all_user_ids(self):
        dir = os.listdir(self.root_path)
        user_ids = []
        for subdir in dir:
            if os.path.isdir(os.path.join(self.root_path, subdir)):
                    try:
                        if int(subdir) < MIN_GUEST_ID:
                            user_ids.append(int(subdir))
                    except Exception:
                        l.exception('user dir not valid: %s', subdir)
        return user_ids
    
    def get_shared(self, user_id, title):
        title = title.encode('utf-8')
        shelf = self._get_shelf(user_id)
        if title not in shelf:
            shelf.close()
            return False
        shared = shelf[title][1]
        return shared
    
    def get_shared_titles(self):
        shared_titles = []
        for user_id in self._get_all_user_ids():
            shelf = self._get_shelf(user_id)
            for title, (filename, shared) in shelf.items():
                if shared:
                    user_details = self.sql_database.get_user_details(user_id)
                    if user_details is not None:
                        user_name = user_details['nickname']
                    else:
                        user_name = 'unknown user'
                    shared_titles.append((user_id, title.decode('utf-8') if isinstance(title, bytes) else title, user_name))
            
        l.debug('shared titles are %s', shared_titles)
        return shared_titles
    
    def get_file(self, user_id, title):
        filename = self._get_filename(user_id, title) 
        user_dir = self._make_user_dir(user_id)
        file_path = os.path.join(user_dir, filename)
        f = codecs.open(file_path, 'rb', encoding='utf-8')
        return f
    
    def _get_filename(self, user_id, title):
        shelf = self._get_shelf(user_id)
        l.debug('shelf is %s', shelf)
        filename = shelf[title][0]
        return filename

    def delete(self, user_id, data):
        document_user_id, title = data.split('/')
        document_user_id = int(document_user_id)
        if user_id != document_user_id:
            raise Exception('You can only delete your own documents')
        title = str(title).encode('utf-8')
        
        shelf = self._get_shelf(user_id)
        if title in shelf:
            user_dir = self._make_user_dir(user_id)
            filename = shelf[title][0]
            file_path = os.path.join(user_dir, filename)
        else:
            raise Exception('The file of name %s is not in your library' % title)
        del shelf[title]
        os.remove(file_path)
        self._save_shelf(user_id)
        return 'Document %s successfully deleted' % title
    
    def share(self, user_id, data):
        document_user_id, title = data.split('/')
        document_user_id = int(document_user_id)
        if user_id != document_user_id:
            raise Exception('You can only share your own documents')
        title = str(title).encode('utf-8')
        shelf = self._get_shelf(user_id)
        details = shelf[title]
        details[1] = True
        shelf[title] = details
        self._save_shelf(user_id)
#        l.debug('shelf is %s', shelf)
        return 'Document %s successfully shared' % title
        
    
    def get_file_page_data(self, user_id, title, page_no):
        """
        Return the page data, number of pages, and if there is a subsequent page or not
        """
        further_pages_available = False
        file = self.get_file(user_id, title)
        initial_read_point = page_no * NUM_BYTES_IN_PAGE
        file.read(initial_read_point)
        data = file.read(NUM_BYTES_IN_PAGE)
        if len(data) >= NUM_BYTES_IN_PAGE:
            # if there is further data then read extra characters until end of current word
            further_pages_available = True
            last_char = data[-1]
            offset = 0
            extra_data = ''
            while last_char not in [' ', '\t', '\n']:
                extra_data = file.read(20)
                last_char = extra_data[offset]
                offset += 1
            data += extra_data[:offset]
        
        filename = self._get_filename(user_id, title)
        user_dir = self._make_user_dir(user_id)
        file_path = os.path.join(user_dir, filename)
        filesize = os.stat(file_path)[6]
        number_of_pages = (filesize // NUM_BYTES_IN_PAGE) + 1
        return {'text': data, 'num_pages' :number_of_pages, 
                'further_pages_available': further_pages_available}
        
    def _make_user_dir(self, user_id):
        """ Ensure that there is a directory under root for this user. Return the 
        path to the user directory """
        dir = os.listdir(self.root_path)
        user_dir = os.path.join(self.root_path, str(user_id))
        if not str(user_id) in dir:
            os.mkdir(user_dir)
        return user_dir
        