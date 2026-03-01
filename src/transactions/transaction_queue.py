
import logging
import threading
import time
import Queue
import atexit

from traits.api import HasTraits, Instance, Int

l = logging.getLogger(__name__)


class TransactionProcessor(threading.Thread):
    
    def __init__(self, queue, commit_interval):
        threading.Thread.__init__(self)
        
        self.stop_flag = False
        self.queue = queue
        self.commit_interval = commit_interval
#        self.cnx = get_connection()
#        self.cursor = self.cnx.cursor()
        atexit.register(self.stop)
        
    def run(self):
        while True:
            self.process_queue()
            if self.stop_flag:
                l.debug('stopping transaction processor')
                self.cnx.commit()
                self.cnx.close()
                return
            time.sleep(self.commit_interval)
            
    def stop(self):
        self.stop_flag = True
    
    def process_queue(self):
        try:
#            l.debug('%s: process queue (%s items)', id(self), self.queue.qsize())
            while not self.queue.empty():
                try:
                    sql, bind_vars = self.queue.get()
                except Queue.Empty, ex:
                    break
                self.cursor.execute(sql, bind_vars)
        except Exception, ex:
            l.exception('logging call (%s)', ex)
        finally:
            pass
#            self.cnx.commit()


class TransactionQueue(HasTraits):
    
    # queue of transactions
    queue = Instance(Queue.Queue, ())
    
    # time, in seconds, between commits
    commit_interval = Int
    
    transaction_processor = Instance(TransactionProcessor)
    
    def __init__(self, **traits):
        super(TransactionQueue, self).__init__(**traits)
        
        self.transaction_processor.start()
        
    def add(self, sql, bind_vars):
        self.queue.put((sql, bind_vars))
        
    def stop(self):
        self.transaction_processor.stop()
    
    def _transaction_processor_default(self):
        transaction_processor = TransactionProcessor(self.queue, self.commit_interval)
        transaction_processor.setDaemon(True)
        return transaction_processor
    
