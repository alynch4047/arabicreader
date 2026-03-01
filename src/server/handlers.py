
import logging

from sqlalchemy import create_engine

from server import configuration

from transactions.api import TransactionQueue
from session_service.api import SessionStore
from sarf_service.api import SarfHandler
from dictionary_service.api import (DictionaryHandler, WordDatabase, SQLDatabase,
                                    Dictionary)
from vocab_db_service.api import VocabDBHandler
from proxy_service.api import ProxyHandler, ProxyCache, ProxyPreFetch
from vocabulary_service.api import VocabularyHandler
from session_service.api import SessionHandler
from control_service.api import ControlHandler
from library_service.api import LibraryHandler, LibraryStore, Searcher
from logger_service.api import LoggerHandler

logger = logging.getLogger(__name__)

# NB there is only one instance of the following 'live' objects
# so they must be thread-safe / reentrant

live_proxy_cache = ProxyCache(proxy_cache_dir=configuration.proxy_cache_dir)
live_proxy_prefetch = ProxyPreFetch(proxy_cache=live_proxy_cache)
live_proxy_prefetch.start()
live_transaction_queue = TransactionQueue(commit_interval=configuration.log_commit_interval)

live_vocabularies = {}
live_engine = create_engine(configuration.sql_connection_string) 
live_sql_database = SQLDatabase(live_engine)
live_library_store = LibraryStore(root_path=configuration.library_store_root,
                              sql_database=live_sql_database)
live_searcher = Searcher(sql_database=live_sql_database,
                         library_store=live_library_store)
live_word_database = WordDatabase(sql_database=live_sql_database)
live_session_store = SessionStore(sql_database=live_sql_database)
live_dictionary = Dictionary(word_database=live_word_database)
# trigger loading of DB before web service starts
print 'There are %s words in the database' % len(live_dictionary.words)


def handlers_factory():
    """ A new handler is instantiated for each request"""
    
    def make_dictionary_handler():
        return DictionaryHandler(dictionary=live_dictionary,
                                 transaction_queue=live_transaction_queue)
    
    def make_vocab_db_handler():
        return VocabDBHandler(dictionary=live_dictionary,
                              word_database=live_word_database)
    
    def make_vocabulary_handler():
        return VocabularyHandler(vocabularies=live_vocabularies,
                                 session_store=live_session_store,
                                 word_database=live_word_database,
                                 sql_database=live_sql_database)
    def make_session_handler():
        return SessionHandler(session_store=live_session_store,
                              sql_database=live_sql_database)
        
    def make_logger_handler():
        return LoggerHandler(sql_database=live_sql_database)
    
    def make_library_handler():
        return LibraryHandler(library_store=live_library_store,
                              sql_database=live_sql_database,
                              searcher=live_searcher)
    
    def make_proxy_handler():
        return ProxyHandler(url_root=configuration.url_root,
                            proxy_cache=live_proxy_cache)
    
    handlers = {
      'sarf':  SarfHandler,
      'dictionary': make_dictionary_handler,
      'modifyword': make_vocab_db_handler,
      'proxy': make_proxy_handler,
      'vocabulary': make_vocabulary_handler,
      'session': make_session_handler,
      'control': ControlHandler,
      'library': make_library_handler,
      'logger': make_logger_handler,
          }
    
    return handlers, live_session_store
