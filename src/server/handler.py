
import logging

import simplejson

from traits.api import HasTraits, Dict

l = logging.getLogger(__name__)


class Handler(HasTraits):
    
    url_lookup = Dict
    
    def get_url(self, url, use_json, session=None, **kwargs):
        for url_key, method in self.url_lookup.items():
            if url.startswith(url_key):
                data = url[len(url_key)+1:]
                if use_json:
                    return self._json_and_wrap_error(method, data, session, **kwargs)
                else:
                    return method(data, session=session, **kwargs)
        else:
            return 'invalid url: %s' % repr(url)
    
    def _json_and_wrap_error(self, func, input_data, session, **kwargs):
        success = 1
        data = ''
        try:
            data = func(input_data, session, **kwargs)
        except Exception, ex:
            l.exception('processing url %s', ex)
            success = 0
            try:
                data = str(ex)
            except:
                data = 'cannot give more details, see server log'
        return_data = {}
        try:
            return_data['num_elements'] = len(data)
        except:
            return_data['num_elements'] = 1
        return_data['success'] = success
        return_data['data'] = data
        json_data = simplejson.dumps(return_data, encoding='utf-8')
        #l.debug('json data is %s', json_data)
        return json_data
            