from string import whitespace


class type1font:
    fontfilename = ''
    fontfiledata = ''
    info = {}
    name = ''
    type = ''
    uniqueID = ''
    eexecdata = ''
    eexecdataplain = ''
    encoding = []
    private = {}
    charstringsdata = ''
    charstrings = {}

    def __init__(self, fontfile):
        self.fontfilename = fontfile
    
    def load(self):
        f = open(self.fontfilename, 'r')
        self.fontfiledata = f.read()
        f.close()
        
    def parse(self):
        """just get eexec data for now, we don't care about any thing else yet (sorry)"""
        eexecpos = self.fontfiledata.find("eexec")
        cleartomarkpos = self.fontfiledata.find("cleartomark")
        # go back from cleartomarkpos getting 512 ascii zeros to find end of eexec data
        numzeros = 0
        pos = cleartomarkpos
        while numzeros < 512:
            #print pos
            pos -= 1
            if self.fontfiledata[pos] == '0':
                numzeros += 1
                eexecendpos = pos

        eexecdataoffset = 12 #  length of word 'eexec' + 6 byte section header
        self.eexecdata = self.fontfiledata[eexecpos + eexecdataoffset:eexecendpos]
        self.eexecdecode(self.eexecdata)
        self.eexecparse()


    def eexecparse(self):
        """ the main thing here is to get the charstrings and decrypt them """
        # find charstringscipher in execdataplain
        charstringspos = self.eexecdataplain.find('/CharStrings')
        beginpos = self.eexecdataplain.find('begin', charstringspos)
        endpos = self.eexecdataplain.find('end', beginpos)
        charstringsoffset = 6
        self.charstringsdata = self.eexecdataplain[beginpos + charstringsoffset:endpos]

        #print repr(self.charstringsdata[0:1000])
        # parse charstrings data
        pos = 0
        charseqno = 0
        while pos <= len(self.charstringsdata) - 1:
            # first check that we have at least one record left
            recfound = self.charstringsdata.find('ND', pos)
            if recfound == -1:
                #print "ND not found",pos,recfound
                break
            recfound = self.charstringsdata.find('RD', pos)
            if recfound == -1:
                #print "RD not found"
                break
            # get char key
            charkey = ''
            while pos <= len(self.charstringsdata):
                if self.charstringsdata[pos] in whitespace:
                    break
                charkey += self.charstringsdata[pos]
                pos += 1
            #print "charkey", charkey, pos
            #eat whitespace
            while pos <= len(self.charstringsdata):
                if self.charstringsdata[pos] not in whitespace:
                    break
                pos += 1
            # get # of binary bytes
            sbytes = ''
            while pos <= len(self.charstringsdata):
                if self.charstringsdata[pos] in whitespace:
                    break
                sbytes += self.charstringsdata[pos]
                numbytes = int(sbytes)
                pos += 1
            #print " num bytes ", numbytes
            #eat whitespace
            while pos <= len(self.charstringsdata):
                if self.charstringsdata[pos] not in whitespace:
                    break
                pos += 1
            # should be 'RD' here
            if self.charstringsdata[pos:pos + 2] != 'RD':
                print "RD ERROR at ", pos
                print repr(self.charstringsdata[pos:pos + 1])
                return
            pos += 2
            #eat whitespace
            while pos <= len(self.charstringsdata):
                if self.charstringsdata[pos] not in whitespace:
                    break
                pos += 1
            # next x bytes are raw data
            chardataraw = self.charstringsdata[pos:pos + numbytes]
            pos += numbytes
            #eat whitespace
            while pos <= len(self.charstringsdata):
                if self.charstringsdata[pos] not in whitespace:
                    break
                pos += 1
            # should be 'ND' here
            if self.charstringsdata[pos:pos + 2] != 'ND':
                print "ND ERROR at ", pos
                return
            pos += 2
            #eat whitespace
            while pos <= len(self.charstringsdata) - 1:
                if self.charstringsdata[pos] not in whitespace:
                    break
                pos += 1
            # should now be at next record, so store current charstring
            self.charstrings[charkey] = (charseqno, numbytes, chardataraw)
            charseqno += 1
  
    def charstringsdecode(self, cipher):
        C1 = 52845
        C2 = 22719
        R = 4330
        plaintext = ''
        for char in cipher: # for each 8-bit byte in the cipher
            T = R >> 8
            P = ord(char) ^ T
            R = (((ord(char) + R) * C1) + C2) % 65536
            plaintext += chr(P)

        return plaintext
    
    def eexecdecode(self, cipher):
        C1 = 52845
        C2 = 22719
        R = 55665
        plaintext = ''
        for char in cipher: # for each 8-bit byte in the cipher
            T = R >> 8
            P = ord(char) ^ T
            R = (((ord(char) + R) * C1) + C2) % 65536
            plaintext += chr(P)

        self.eexecdataplain = plaintext
        return plaintext

    def eexecencode(self, plain):
        C1 = 52845
        C2 = 22719
        R = 55665
        ciphertext = ''
        for char in plain: # for each 8-bit byte in the cipher
            T = R >> 8
            P = ord(char) ^ T
            R = (((P + R) * C1) + C2) % 65536
            ciphertext += chr(P)
        
        return ciphertext


    def loadAFM(self, AFMFileName):
        self.charWidths = {}
        self.charSize = {}
        f = open(AFMFileName)
        for line in f.readlines():
            data = line.split()
            if data[0] == 'C':
                self.charWidths[data[7]] = int(data[4])
                self.charSize[data[7]] = (data[10], data[11], data[12], data[13])
        

