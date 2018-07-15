'''MSP430 MCUs'''
# mcu build scripts based on scons, designed by PengShulin 
# Peng Shulin <trees_peng@163.com> 2018
from Toolchain import Gcc
from VEnvironment import VEnvironment, hal_config

class Msp430Gcc(Gcc):
    PREFIX = 'msp430-'

class Msp430(VEnvironment):
    '''base class for msp430 mcus'''
    mcu = ''
    _TOOLCHAIN = Msp430Gcc
    _CCFLAGS = ['-mcpu=430x']
    _CPPPATH = []
    _LIBPATH = []
    _LIBS = []
    _LINKFLAGS = ['-mcpu=430x']

    def __init__( self ):
        VEnvironment.__init__( self )
        if self.mcu:
            self.appendCompilerFlag( ['-mmcu=%s'% self.mcu] )
            self.appendLinkFlag( ['-mmcu=%s'% self.mcu] )
        

class Msp430F47163(Msp430):
    mcu = 'msp430f47163'

class Msp430FG4616(Msp430):
    mcu = 'msp430fg4616'




