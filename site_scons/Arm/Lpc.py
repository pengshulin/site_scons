'''nxp series'''
# mcu build scripts based on scons, designed by PengShulin 
from Cortex import CortexM0, CortexM3, CortexM4, CortexM7
from Cortex import CMSIS_DSP_Driver
from VEnvironment import Driver

# TODO: support LPC43xx LPC2xxx ...

class Lpc43xx(CortexM4):
    def __init__( self, drivers=None ):
        CortexM4.__init__( self )
        self.appendDrivers( drivers )

class Lpc43xx_StartupDriver(Driver):
    def __init__(self, cpu):
        self.SOURCE = [
            '/NXP/startup/cr_startup_lpc43xx.c', 
            '/NXP/startup/sysinit.c', ]

class Lpc43xx_ChipDriver(Driver):
    PATH = ['/NXP/lpcopen/lpc_chip_43xx/inc']
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


class Lpc4337m0(CortexM0):
    pass


