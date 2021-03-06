'''ATMEL AVR Series'''
# MCUSH Scons Build Scripts, designed by Peng Shulin 
from Toolchain import Gcc
from VEnvironment import VEnvironment, hal_config

class AvrGcc(Gcc):
    PREFIX = 'avr-'


class Avr(VEnvironment):
    '''base class for avr'''
    mcu = ''
    _TOOLCHAIN = AvrGcc
    _CCFLAGS = ['-gdwarf-2', '-funsigned-char',
                '-funsigned-bitfields', '-fpack-struct', '-fshort-enums', ]
    _CPPPATH = []
    _LIBPATH = []
    _LIBS = []
    _LINKFLAGS = []

    def __init__( self ):
        VEnvironment.__init__( self )
        if self.mcu:
            self.appendCompilerFlag( ['-mmcu=%s'% self.mcu] )
            self.appendLinkFlag( ['-mmcu=%s'% self.mcu] )
        

class Atmega128(Avr):
    mcu = 'atmega128'

