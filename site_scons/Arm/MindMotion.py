'''Cortex-M0/M3 based MCU from Shanghai MindMotion Microelectronics'''
# MCUSH Scons Build Scripts, designed by Peng Shulin 
from Cortex import CortexM0, CortexM3
from Cortex import CMSIS_DSP_Driver
from VEnvironment import Driver, hal_config


# Startup driver
class MM32F0_StartupDriver(Driver):
    PATH = ['/MindMotion/mm32f0/startup/inc']
    def __init__(self, mcu_class):
        self.SOURCE = [
            '/MindMotion/mm32f0/startup/startup_mm32.c',
            '/MindMotion/mm32f0/startup/system_mm32.c' ]
        self.CFLAG = []
        self.CFLAG.append( '-D%s'% mcu_class )
        self.LDFLAG = ['-Wl,--entry=Reset_Handler'] 

class MM32F103_StartupDriver(Driver):
    PATH = ['/MindMotion/mm32f103/Include']
    def __init__(self, mcu_class):
        self.SOURCE = [
            '/MindMotion/mm32f103/Source/startup_mm32.c',
            '/MindMotion/mm32f103/Source/system_MM32F103.c' ]
        self.CFLAG = []
        self.CFLAG.append( '-D%s'% mcu_class )
        self.LDFLAG = ['-Wl,--entry=Reset_Handler'] 



# HAL lib
class MM32F0_HAL_lib(Driver):
    PATH = ['/MindMotion/mm32f0/HAL_lib/inc']
    GLOBSOURCE = ['/MindMotion/mm32f0/HAL_lib/*.c']
    CFLAG = []

class MM32F103_HAL_lib(Driver):
    PATH = ['/MindMotion/mm32f103/HAL_lib/inc']
    GLOBSOURCE = ['/MindMotion/mm32f103/HAL_lib/src/*.c']
    CFLAG = ['-DUSE_STDPERIPH_DRIVER']



#############################################################################
# CHIPS BELOW
#############################################################################

class MM32M0(CortexM0):
    def __init__( self, drivers=None ):
        CortexM0.__init__( self )
        self.appendDrivers( drivers )

class MM32M3(CortexM3):
    def __init__( self, drivers=None ):
        CortexM3.__init__( self )
        self.appendDrivers( drivers )

# MCU class macro defination
# __MM3N1  Cortex-M3  MM32F103 / MM32L3xx  
# __MM0N1  Cortex-M0  MM32F031x8, xB/MM32L0xx  
# __MM0P1  Cortex-M0  MM32SPIN2x  
# __MM0Q1  Cortex-M0  MM32F003 / MM32F031x4,x6  

# MM32F031x8
class MM32F031x8(MM32M0):
    def __init__(self):
        MM32M0.__init__( self, drivers=[
            MM32F0_StartupDriver('__MM0N1'),
            MM32F0_HAL_lib() ] )

# MM32F103x8
class MM32F103x8(MM32M3):
    def __init__(self):
        MM32M3.__init__( self, drivers=[
            #MM32F103_StartupDriver('__MM3N1'),
            #MM32F103_HAL_lib() ] )
            MM32F0_StartupDriver('__MM3N1'),
            MM32F0_HAL_lib() ] )
        # NOTE: irq priority write/read does not match when PRIO_BITS is set 4
        # so use PRIO_BITS=3 instead, confirm PriorityGroup is also configured
        self.appendCompilerFlag( ['-D__NVIC_PRIO_BITS=3'] )


