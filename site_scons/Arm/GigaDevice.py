'''Cortex-M3/M4 MCU from GigaDevice Semiconductor Inc.'''
# MCUSH Scons Build Scripts, designed by Peng Shulin 
from Cortex import CortexM3, CortexM4
from Cortex import CMSIS_DSP_Driver
from VEnvironment import Driver, hal_config


# Startup driver
class GD32F10X_StartupDriver(Driver):
    PATH = ['/CMSIS/Device/GD/GD32F10x/Include/']
    def __init__(self, density):
        assert density in ['md', 'hd', 'xd', 'cl']
        self.SOURCE = [
            '/CMSIS/Device/GD/GD32F10x/Source/system_gd32f10x.c' ]
        self.CFLAG = ['-DGD32F10X_%s'% density.upper()]
        self.LDFLAG = ['-Wl,--entry=__vector_table'] 


# Standard Peripheral driver
class GD32F10X_StdPeripheralDriver(Driver):
    PATH = ['/GD/GD32F10x_standard_peripheral/Include']
    GLOBSOURCE = ['/GD/GD32F10x_standard_peripheral/Source/*.c']
    CFLAG = []


#############################################################################
# CHIPS BELOW
#############################################################################

class GD32M3(CortexM3):
    def __init__( self, drivers=None ):
        CortexM3.__init__( self )
        self.appendDrivers( drivers )

# MCU class macro defination

# GD32F103x8
class GD32F103x8(GD32M3):
    def __init__(self):
        GD32M3.__init__( self, drivers=[
            GD32F10X_StartupDriver('md'),
            GD32F10X_StdPeripheralDriver() ] )



