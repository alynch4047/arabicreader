
import ar_logging

import logging
l = logging.getLogger(__name__)

def server_out(output):
    message = output or "None"
    if len(message) > 100:
        message = message[:100]
    l.info('OUT: %s', message)
    return output