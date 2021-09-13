'''NXP LPC Series'''
# MCUSH Scons Build Scripts, designed by Peng Shulin 
from Cortex import CortexM0, CortexM3, CortexM4, CortexM7
from Cortex import CMSIS_DSP_Driver
from VEnvironment import Driver, hal_config



class Lpc84x(CortexM0):
    def __init__( self, drivers=None ):
        CortexM0.__init__( self )
        self.appendDrivers( drivers )

class Lpc84x_StartupDriver(Driver):
    def __init__(self, cpu):
        self.PATH = ['/CMSIS/Device/NXP/lpc84x']
        self.SOURCE = [
            '/CMSIS/Device/NXP/lpc84x/startup/startup_lpc845.c', 
            '/CMSIS/Device/NXP/lpc84x/system_LPC845.c', ]

class FSL_Driver(Driver):
    PATH = ['/NXP/fsl']
    GLOBSOURCE = ['/NXP/fsl/*.c']


class Lpc845M301JBD48(Lpc84x):
    cpu = 'LPC845M301JBD48'
    def __init__(self, startup_driver=True, chip_driver=True):
        drivers=[]
        if startup_driver:
            drivers.append( Lpc84x_StartupDriver(self.cpu) )
        if chip_driver:
            drivers.append( FSL_Driver() )
        Lpc84x.__init__( self, drivers=drivers )
        self.appendCompilerFlag( ['-DCPU_%s'% (self.cpu.upper())] )





class Lpc43xx(CortexM4):
    def __init__( self, drivers=None ):
        CortexM4.__init__( self )
        self.appendDrivers( drivers )

class Lpc43xx_StartupDriver(Driver):
    def __init__(self, cpu):
        self.SOURCE = [
            '/CMSIS/Device/NXP/lpc43xx/startup/cr_startup_lpc43xx.c', 
            '/CMSIS/Device/NXP/lpc43xx/startup/sysinit.c', ]

class Lpc43xx_ChipDriver(Driver):
    PATH = ['/NXP/lpcopen/lpc_chip_43xx/inc',
            '/NXP/lpcopen/lpc_chip_43xx/inc/config_43xx' ]
    GLOBSOURCE = ['/NXP/lpcopen/lpc_chip_43xx/src/*.c']


class Lpc4337(Lpc43xx):
    cpu = 'LPC4337'
    def __init__(self, startup_driver=True, chip_driver=True):
        drivers=[]
        if startup_driver:
            drivers.append( Lpc43xx_StartupDriver(self.cpu) )
        if chip_driver:
            drivers.append( Lpc43xx_ChipDriver() )
        Lpc43xx.__init__( self, drivers=drivers )
        #self.appendCompilerFlag( ['-D__CHECK_DEVICE_DEFINES=1'] )
        self.appendCompilerFlag( ['-D__NVIC_PRIO_BITS=3'] )
        self.appendCompilerFlag( ['-D__USE_LPCOPEN'] )



class Lpc4337m0(CortexM0):
    pass



