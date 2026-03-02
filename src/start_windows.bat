set PATH=C:\Program Files (x86)\Java\jre6\bin;c:\optpython25\;%PATH%
set PWD=c:\Users\alynch\workspace\arabicreader
set JARS=%PWD%\jars
set WEBDIR=%PWD%\static\applications
del c:\temp\arlogging.log
python build.py
copy %WEBDIR%\arabic_reader.js %WEBDIR%\arabic_reader_uncompressed.js
java -jar %JARS%\yuicompressor-2.3.5.jar  %WEBDIR%\arabic_reader.js -o %WEBDIR%\arabic_reader.js                             
python run_server.py -c local.windows.config

