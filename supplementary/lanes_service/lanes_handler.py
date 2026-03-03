


class LanesHandler(object):
    
    def get_url(self, url):
            if url.startswith('page/'):
                return self._get_page(url[5:])
            elif url.startswith('root/'):
                return self._get_root_info(url[5:])
            else:
                return 'invalid url'
            
    def _get_page(self, page_no):
        return ' you requested lanes pg %s' % page_no
    
    def _get_root_info(self, root):
        root = root.decode('utf-8') if isinstance(root, bytes) else root
        chars_in_root = len(root)
        root_faa = root[0]
        root_ayn = root[1]
        root_lam = root[2]
        
        return '<P> %s %s %s</P><P> means Praise2</P>' %\
               (root_faa, root_ayn, root_lam)