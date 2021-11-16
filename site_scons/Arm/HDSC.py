'''Cortex-M0/M4 MCU from Huada Semiconductor Inc.'''
# MCUSH Scons Build Scripts, designed by Peng Shulin 
from Cortex import CortexM0, CortexM4
from Cortex import CMSIS_DSP_Driver
from VEnvironment import Driver, hal_config


# Startup driver
class HC32F030_StartupDriver(Driver):
    PATH = ['/HDSC/hc32f030/common/']
    def __init__(self, package_define):
        self.SOURCE = [ '/HDSC/hc32f030/common/system_hc32f030.c',
                        '/HDSC/hc32f030/common/startup_hc32f030.c' ]
        self.CFLAG = ['-D%s'% package_define]
        self.LDFLAG = ['-Wl,--entry=__vector_table'] 


# Standard Peripheral driver
class HC32F030_StdPeripheralDriver(Driver):
    PATH = ['/HDSC/hc32f030/inc']
    GLOBSOURCE = ['/HDSC/hc32f030/src/*.c']
    CFLAG = []


#############################################################################
# CHIPS BELOW
#############################################################################

class HC32F0(CortexM0):
    def __init__( self, drivers=None ):
        CortexM0.__init__( self )
        self.appendDrivers( drivers )

# MCU class macro defination

# HC32F030x8
class HC32F030x8(HC32F0):
    def __init__(self):
        HC32F0.__init__( self, drivers=[
            HC32F030_StartupDriver(package_define=self.PACKAGE_DEFINE),
            HC32F030_StdPeripheralDriver() ] )

class HC32F030K8(HC32F030x8):  # 64pin
    PACKAGE_DEFINE = 'HC32F030Kxxx'

class HC32F030J8(HC32F030x8):  # 48pin
    PACKAGE_DEFINE = 'HC32F030Jxxx'

class HC32F030H8(HC32F030x8):  # 44pin
    PACKAGE_DEFINE = 'HC32F030Hxxx'

class HC32F030F8(HC32F030x8):  # 32pin
    PACKAGE_DEFINE = 'HC32F030Fxxx'

class HC32F030E8(HC32F030x8):  # 28pin
    PACKAGE_DEFINE = 'HC32F030Exxx'


