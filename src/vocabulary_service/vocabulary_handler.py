
import logging
import cherrypy

from traits.api import Instance

from server.api import Handler
from session_service.api import SessionStore
from dictionary_service.api import WordDatabase, SQLDatabase

from vocabulary_service.vocabulary import Vocabulary
from vocabulary_service.create_pdf import VocabPDF, TestVocabPDF

l = logging.getLogger(__name__)


class VocabularyHandler(Handler):
    
    session_store = Instance(SessionStore)
    
    word_database = Instance(WordDatabase)
    
    sql_database = Instance(SQLDatabase)
    
    def __init__(self, vocabularies, **traits):
        Handler.__init__(self, **traits)
        self.vocabularies = vocabularies
    
    def _url_lookup_default(self):
        lookup = {
                  'allwords': self._get_all_words,
                  'addword' : self._add_word,
                  'removeword' : self._remove_word,
                  'vocab.pdf': self._get_vocab_pdf,
                  'test.pdf': self._get_test_pdf,
        }
        return lookup
    
    def _get_all_words(self, data, session):
        return self._get_vocabulary(session).get_all_word_ids()
    
    def _add_word(self, data, session):
        if not session.authenticated:
            raise Exception('cannot add vocab - not authenticated')
        word_id = data
        return self._get_vocabulary(session).add_word(word_id)
    
    def _remove_word(self, data, session):
        if not session.authenticated:
            raise Exception('cannot remove vocab - not authenticated')
        word_id = data
        return self._get_vocabulary(session).remove_word(word_id)
            
    def _get_vocabulary(self, session):
        if session not in self.vocabularies:
            l.debug('add new vocabulary list to %s for unknown session %s', id(self.vocabularies),
                    session)
            self.vocabularies[session] = Vocabulary(session=session,
                                                    word_database=self.word_database,
                                                    sql_database=self.sql_database)
        l.debug('return vocab %s', self.vocabularies[session])
        return self.vocabularies[session]
    
    def _get_vocab_pdf(self, data, session):
        cherrypy.response.headers['Content-Type'] = "text/pdf"
        vocabulary = self._get_vocabulary(session)
        return VocabPDF(user_id=session.user_id,
                        vocabulary=vocabulary).create_pdf()
                        
    def _get_test_pdf(self, data, session):
        cherrypy.response.headers['Content-Type'] = "text/pdf"
        return TestVocabPDF(user_id=session.user_id).create_pdf()
    
