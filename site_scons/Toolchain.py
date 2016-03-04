'''toolchain defination'''

class Gcc():
    '''base toochain'''
    PREFIX = ''
    AR = 'ar'
    AS = 'as'
    CC = 'gcc'
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
        self.AR = self.PREFIX + self.AR
        self.AS = self.PREFIX + self.AS
        self.LINK = self.PREFIX + self.LINK
        self.NM = self.PREFIX + self.NM
        self.RANDLIB = self.PREFIX + self.RANDLIB
        self.OBJCOPY = self.PREFIX + self.OBJCOPY
        self.OBJDUMP = self.PREFIX + self.OBJDUMP
        self.SIZE = self.PREFIX + self.SIZE

class ArmNoneEabiGcc(Gcc):
    PREFIX = 'arm-none-eabi-'

class ArmElfGcc(Gcc):
    PREFIX = 'arm-elf-'

class Msp430Gcc(Gcc):
    PREFIX = 'msp430-'



