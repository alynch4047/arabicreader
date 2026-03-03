import logging

from constants import *

def psOut(text):
    global psFile
    try:
        logging.debug('ps out %s', text)
        psFile.write(text + '\n')
    except:
        print("exception text is", repr(text))
        raise

def postscriptProlog():
    global psFile, encode
    psFileName = 'psout.ps'
    psFile = open(psFileName,'w')
    psPrologFileName = 'prolog.ps'
    psPrologFile = open(psPrologFileName,'r')

              
    psOut('/haqqenc [')

    for code in encoding:
        psOut(code)
    
    psOut('] def')

    l = psPrologFile.readline()
    while l:
        psFile.write(l)
        l = psPrologFile.readline()

def postscriptEpilog():
    global psFile
    psFile.close()

def paginate():
    """ paginate the ps file """
    global psFile
    
def main():
    postscriptProlog()

if __name__ == '__main__':
    main()
