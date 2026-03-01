
import os
import logging
from optparse import OptionParser

from server.configobj import ConfigObj

l = logging.getLogger(__name__)

parser = OptionParser()
parser.add_option("-c", dest="config_filepath",
                  help="path to configuration file")

options, args = parser.parse_args()

if options.config_filepath is None:
    if 'AR_CONFIG_FILE' in os.environ:
        configuration_file_path = os.environ['AR_CONFIG_FILE']
    else:
        raise Exception('You must specify the location of the configuration file')
else:
    configuration_file_path = options.config_filepath
if not os.path.isfile(configuration_file_path):
    raise Exception('No configuration file found at %s' % configuration_file_path)

l.debug('load configuration from %s', configuration_file_path)
config = ConfigObj(configuration_file_path)

# configuration settings
library_store_root = config['locations']['library_store_root']
l.debug('library store root: %s', library_store_root)

log_commit_interval = int(config['logging']['log_commit_interval'])
l.debug('log commit interval: %ss', log_commit_interval)

url_root = config['proxy']['url_root']

proxy_cache_dir = config['proxy']['cache_dir']
l.debug('proxy cache dir: %s', proxy_cache_dir)

session_always_authenticated = config['session']['always_authenticated'].upper() == 'TRUE'

sql_connection_string = config['sql']['connection_string']

log_file = config['logging']['log_file']

port = int(config['proxy']['port'])
