'''MSP430 MCUs'''
from Toolchain import Gcc
from VEnvironment import VEnvironment

class Msp430Gcc(Gcc):
    PREFIX = 'msp430-'

class Msp430(VEnvironment):
    '''base class for msp430 mcus'''
    mcu = ''
    _TOOLCHAIN = Msp430Gcc
    _CCFLAGS = ['-Wno-unused-but-set-variable', '-Wall', '-mcpu=430x']
    _CPPPATH = []
    _LIBPATH = []
    _LIBS = []
    _LINKFLAGS = ['-mcpu=430x', '-Wl,--gc-sections']

    def __init__( self ):
        VEnvironment.__init__( self )
        if self.mcu:
            self.appendCompilerFlag( ['-mmcu=%s'% self.mcu] )
            self.appendLinkFlag( ['-mmcu=%s'% self.mcu] )
        

class Msp430F47163(Msp430):
    mcu = 'msp430f47163'
