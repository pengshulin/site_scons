'''cortex-m3 based controller'''
from Toolchain import Gcc
from VEnvironment import VEnvironment

class ArmNoneEabiGcc(Gcc):
    PREFIX = 'arm-none-eabi-'

class ArmElfGcc(Gcc):
    PREFIX = 'arm-elf-'

class CortexM3(VEnvironment):
    '''base class for cortex-m3'''
    _TOOLCHAIN = ArmNoneEabiGcc
    _CCFLAGS = ['-mcpu=cortex-m3' ,'-mthumb', '-Wall' ]
    _CPPPATH = []
    _LIBPATH = []
    _LIBS = []
    _LINKFLAGS = ['-mcpu=cortex-m3', '-mthumb', '-Wl,--gc-sections']

    def __init__( self ):
        VEnvironment.__init__( self )
        self.appendPath( ['/CMSIS/Include'] )


