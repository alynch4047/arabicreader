import os
import re

build_list = [('static/applications/','arabic_reader.js.source', 'arabic_reader.js'),
              ('static/applications/','new_definition.source.html', 'new_definition.html'),
              ('static/applications/','revise.source.html', 'revise.html'),
              ('static/applications/','login.source.html', 'login.html'),
              ('static/applications/','central_text.source.html', 'central_text.html'),
              ('static/applications/','arabic_reader_body.source.html', 'arabic_reader_body.html'),
              ('static/applications/','arabic_reader.source.html', 'arabic_reader.html'),
              ('static/applications/','arabic_reader_debug.source.html',
                                                         'arabic_reader_debug.html'),
              ('static/applications/','arabic_reader_aol.source.html',
                                                         'arabic_reader_aol.html'),
              ('static/applications/','ff_extension.source.html', 'ff_extension.html'),                                           
              ]


def build(directory, build_file):
    cwd = os.getcwd()
    text = open(os.path.join(cwd, directory, build_file)).read()
    include_files = re.compile('<#include (.*)#>').findall(text)
    for include_file in include_files:
        include_file_text = open(os.path.join(cwd, directory, include_file)).read()
        spacing = 0
        for line in text.split('\n'):
            line = line.replace('\t', ' ' * 4)
            if line.find('<#include %s#>' % include_file) != -1:
                spacing = line.find('<#include %s#>' % include_file)
                break
        if spacing:
            new_include_file_text = ''
            for line in include_file_text.split('\n'):
                if line:
                    line = line.replace('\t', ' ' * 4)
                    new_include_file_text += ' ' * spacing + line + '\n'
            include_file_text = new_include_file_text
        text = text.replace('<#include %s#>' % include_file, include_file_text)
    return text

def run():
    for build_dir, build_source, build_file in build_list:
        out_text = build(build_dir, build_source)
        cwd = os.getcwd()
        f = open(os.path.join(cwd, build_dir, build_file), 'wb')
        f.write(out_text)
        f.close()
        
        
if __name__ == '__main__':
    run()