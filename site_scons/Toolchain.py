'''toolchain defination'''
# mcu build scripts based on scons, designed by PengShulin 
# Peng Shulin <trees_peng@163.com> 2018

class Gcc():
    '''base toochain'''
    PREFIX = ''
    AR = 'ar'
    AS = 'as'
    CC = 'gcc'
    CXX = 'g++'
    LINK = 'gcc'
    NM = 'nm'
    RANDLIB = 'randlib'
    OBJCOPY = 'objcopy'
    OBJDUMP = 'objdump'
    SIZE = 'size'

    def __init__( self, prefix=None ):
        if prefix:
            self.PREFIX = prefix
        self.CC = self.PREFIX + self.CC
        self.CXX = self.PREFIX + self.CXX
        self.AR = self.PREFIX + self.AR
        self.AS = self.PREFIX + self.AS
        self.LINK = self.PREFIX + self.LINK
        self.NM = self.PREFIX + self.NM
        self.RANDLIB = self.PREFIX + self.RANDLIB
        self.OBJCOPY = self.PREFIX + self.OBJCOPY
        self.OBJDUMP = self.PREFIX + self.OBJDUMP
        self.SIZE = self.PREFIX + self.SIZE



