'''cortex-m3 based controller'''
from Toolchain import Msp430Gcc
from VEnvironment import VEnvironment


class Msp430(VEnvironment):
    '''base class for cortex-m3'''
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

