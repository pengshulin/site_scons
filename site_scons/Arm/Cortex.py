'''cortex based controller'''
# mcu build scripts based on scons, designed by PengShulin 
from Toolchain import Gcc
from VEnvironment import VEnvironment, Driver

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
    _EXTRA_CCFLAGS = []
    _EXTRA_LINKFLAGS = []

    def __init__( self, cmsis_inc=True ):
        VEnvironment.__init__( self )
        assert self._MCPU
        # NOTE: 
        # link flags must contain cpu/fpu configs same as compiler flags,
        # which will influence how the ld is called and which libs are used
        self.appendCompilerFlag( ['-mcpu=%s'%self._MCPU, '-mthumb'] )
        self.appendLinkFlag( ['-mcpu=%s'%self._MCPU, '-mthumb'] )
        if cmsis_inc:
            self.appendPath( ['/CMSIS/Include'] )
        self.appendCompilerFlag(self._EXTRA_CCFLAGS)
        self.appendLinkFlag(self._EXTRA_LINKFLAGS)
        #self.appendLinkFlag(['-v'])  # to check how ld is called by gcc
        #self.appendCompilerFlag( ['-print-libgcc-file-name'] )
        #self.appendCompilerFlag(['-fsingle-precision-constant'])


class CortexM0(Cortex):
    _MCPU = 'cortex-m0'
    _EXTRA_CCFLAGS = ['-mfloat-abi=soft']

class CortexM0plus(Cortex):
    _MCPU = 'cortex-m0plus'
    _EXTRA_CCFLAGS = ['-mfloat-abi=soft']

class CortexM3(Cortex):
    _MCPU = 'cortex-m3'
    _EXTRA_CCFLAGS = ['-mfloat-abi=soft']

class CortexM4(Cortex):
    _MCPU = 'cortex-m4'
    _EXTRA_CCFLAGS = ['-mfloat-abi=hard', '-mfpu=fpv4-sp-d16', ]
    _EXTRA_LINKFLAGS = ['-mfloat-abi=hard', '-mfpu=fpv4-sp-d16', ]

class CortexM7(Cortex):
    _MCPU = 'cortex-m7'
    _EXTRA_CCFLAGS = ['-mfloat-abi=hard', '-mfpu=fpv4-sp-d16']
    _EXTRA_LINKFLAGS = ['-mfloat-abi=hard', '-mfpu=fpv4-sp-d16']


# CMSIS-DSP driver
class CMSIS_DSP_Driver(Driver):

    def __init__(self, cpu, fpu=False, fpu_double=False, source=False):
        if cpu == 'cortex-m0':
            self.CFLAG = ['-DARM_MATH_CM0']
            fpu = False
        elif cpu == 'cortex-m0plus':
            self.CFLAG = ['-DARM_MATH_CM0PLUS']
            fpu = False
        elif cpu == 'cortex-m3':
            self.CFLAG = ['-DARM_MATH_CM3']
            fpu = False
        elif cpu == 'cortex-m4':
            self.CFLAG = ['-DARM_MATH_CM4']
        elif cpu == 'cortex-m7':
            self.CFLAG = ['-DARM_MATH_CM7']
        if fpu:
            self.CFLAG += ['-D__VFP_FP__', '-D__FPU_PRESENT']
        if source:
            self.GLOBSOURCE = [
                '/CMSIS/DSP_Lib/Source/BasicMathFunctions/*.c',
                '/CMSIS/DSP_Lib/Source/ComplexMathFunctions/*.c',
                '/CMSIS/DSP_Lib/Source/FastMathFunctions/*.c',
                '/CMSIS/DSP_Lib/Source/MatrixFunctions/*.c',
                '/CMSIS/DSP_Lib/Source/SupportFunctions/*.c',
                '/CMSIS/DSP_Lib/Source/CommonTables/*.c',
                '/CMSIS/DSP_Lib/Source/ControllerFunctions/*.c',
                '/CMSIS/DSP_Lib/Source/FilteringFunctions/*.c',
                '/CMSIS/DSP_Lib/Source/StatisticsFunctions/*.c',
                '/CMSIS/DSP_Lib/Source/TransformFunctions/*.c',
                '/CMSIS/DSP_Lib/Source/TransformFunctions/*.S',
                ]
        else:
            self.LIBPATH = ['/CMSIS/Lib/GCC']
            if cpu in ['cortex-m0', 'cortex-m0plus']:
                self.LIB = ['arm_cortexM0l_math']
            elif cpu == 'cortex-m3':
                self.LIB = ['arm_cortexM3l_math']
            elif cpu == 'cortex-m4':
                if fpu:
                    self.LIB = ['arm_cortexM4lf_math']
                else:
                    self.LIB = ['arm_cortexM4l_math']
            elif cpu == 'cortex-m7':
                if fpu:
                    if fpu_double:
                        self.LIB = ['arm_cortexM7lfdp_math']
                    else:
                        self.LIB = ['arm_cortexM7lfsp_math']
                else:
                    self.LIB = ['arm_cortexM7l_math']





