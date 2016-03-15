'''cortex based controller'''
from Toolchain import Gcc
from VEnvironment import VEnvironment

class ArmNoneEabiGcc(Gcc):
    PREFIX = 'arm-none-eabi-'

class Cortex(VEnvironment):
    '''base class for cortex'''
    _TOOLCHAIN = ArmNoneEabiGcc
    _MCPU = None
    _CCFLAGS = []
    _CPPPATH = []
    _LIBPATH = []
    _LIBS = []
    _LINKFLAGS = []

    def __init__( self ):
        VEnvironment.__init__( self )
        assert self._MCPU
        self.appendCompilerFlag( ['-mcpu=%s'%self._MCPU, '-mthumb'] )
        self.appendLinkFlag( ['-mcpu=%s'%self._MCPU, '-mthumb'] )
        self.appendPath( ['/CMSIS/Include'] )


class CortexM0(Cortex):
    _MCPU = 'cortex-m0'

class CortexM3(Cortex):
    _MCPU = 'cortex-m3'

class CortexM4(Cortex):
    _MCPU = 'cortex-m4'



