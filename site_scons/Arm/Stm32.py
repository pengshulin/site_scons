'''stm32 series'''
from Cortex import CortexM3


class Driver():
    USE = True
    PATH = []
    SOURCE = []
    GLOBSOURCE = []
    CFLAG = []
    LIBPATH = []
    LIB = []
    LDFLAG = []

# Startup driver
class STM32F10X_StartupDriver(Driver):
    PATH = ['/CMSIS/Device/ST/STM32F10x/Include']
    def __init__(self, density):
        assert density in ['md', 'hd', 'ld', 'ld_vl']
        self.SOURCE = [
            '/CMSIS/Device/ST/STM32F10x/Source/Templates/gcc_ride7/startup_stm32f10x_%s.s'% density, 
            '/CMSIS/Device/ST/STM32F10x/Source/Templates/system_stm32f10x.c' ]
        self.CFLAG = ['-DSTM32F10X_%s'% density.upper()]
        self.LDFLAG = ['--entry', 'Reset_Handler'] 

class STM32L1XX_StartupDriver(Driver):
    PATH = ['/CMSIS/Device/ST/STM32L1xx/Include']
    def __init__(self, density):
        assert density in ['md', 'mdp', 'hd']
        self.SOURCE = [
            '/CMSIS/Device/ST/STM32L1xx/Source/Templates/gcc_ride7/startup_stm32l1xx_%s.s'% density, 
            '/CMSIS/Device/ST/STM32L1xx/Source/Templates/system_stm32l1xx.c' ]
        self.CFLAG = ['-DSTM32L1XX_%s'% density.upper()]
        self.LDFLAG = ['--entry', 'Reset_Handler'] 

class STM32F2XX_StartupDriver(Driver):
    PATH = ['/CMSIS/Device/ST/STM32F2xx/Include']
    def __init__(self):
        self.SOURCE = [
            '/CMSIS/Device/ST/STM32F2xx/Source/Templates/gcc_ride7/startup_stm32f2xx.s', 
            '/CMSIS/Device/ST/STM32F2xx/Source/Templates/system_stm32f2xx.c' ]
        self.CFLAG = []
        self.LDFLAG = ['--entry', 'Reset_Handler'] 

# Standard Peripheral driver
class STM32F10X_StdPeripheralDriver(Driver):
    PATH = ['/ST/STM32F10x_StdPeriph_Driver/inc']
    GLOBSOURCE = ['/ST/STM32F10x_StdPeriph_Driver/src/*.c']
    CFLAG = ['-DUSE_STDPERIPH_DRIVER']

class STM32L1XX_StdPeripheralDriver(Driver):
    PATH = ['/ST/STM32L1xx_StdPeriph_Driver/inc']
    GLOBSOURCE = ['/ST/STM32L1xx_StdPeriph_Driver/src/*.c']
    CFLAG = ['-DUSE_STDPERIPH_DRIVER']

class STM32F2XX_StdPeripheralDriver(Driver):
    PATH = ['/ST/STM32F2xx_StdPeriph_Driver/inc']
    GLOBSOURCE = ['/ST/STM32F2xx_StdPeriph_Driver/src/*.c']
    CFLAG = ['-DUSE_STDPERIPH_DRIVER']

# USB Full Speed driver
class STM32_USB_FS_Driver(Driver):
    PATH = ['/ST/STM32_USB-FS-Device_Driver/inc']
    GLOBSOURCE = ['/ST/STM32_USB-FS-Device_Driver/src/*.c']

# Touch Driver
class STM32_Touch_Driver(Driver):
    PATH = ['/ST/STMTouch_Driver/inc', '/ST/STMTouch_Driver/inc/to adapt']
    GLOBSOURCE = ['/ST/STMTouch_Driver/src/*.c']

# EVAL Board Driver
class STM32_EVAL_Driver(Driver):
    def __init__(self):
        self.PATH = ['/ST/STM32_EVAL/%s'% self.NAME.upper(),
                     '/ST/STM32_EVAL/Common', ]
        self.GLOBSOURCE = ['/ST/STM32_EVAL/%s/*.c'% self.NAME.upper()]
        self.CFLAG = ['-DUSE_%s'% self.NAME.upper()]

class STM3210B_EVAL_Driver(STM32_EVAL_Driver):
    NAME = 'STM3210B_EVAL'

class STM3210E_EVAL_Driver(STM32_EVAL_Driver):
    NAME = 'STM3210E_EVAL'

class STM32L152_EVAL_Driver(STM32_EVAL_Driver):
    NAME = 'STM32L152_EVAL'

class STM32L152D_EVAL_Driver(STM32_EVAL_Driver):
    NAME = 'STM32L152D_EVAL'

class STM32303C_EVAL_Driver(STM32_EVAL_Driver):
    NAME = 'STM32303C_EVAL'

class STM32373C_EVAL_Driver(STM32_EVAL_Driver):
    NAME = 'STM32373C_EVAL'

# STemWin
# NOTE: symbolic link libSTemWin.a needs to be created manually
class STemWin(Driver):
    PATH = ['/ST/STemWin/inc']
    LIBPATH = ['/ST/STemWin/Lib']
    LIB = ['STemWin.a']




    
# base class
class Stm32(CortexM3):
    DRIVERS = {}
    def __init__( self, drivers=None ):
        CortexM3.__init__( self )
        if drivers is None:
            drivers = self.DRIVERS
        for d in drivers: 
            self.appendDriver(d)

    def appendDriver(self, d):
        if d.USE:
            self.appendPath( d.PATH )
            self.appendLibPath( d.LIBPATH )
            self.appendLib( d.LIB )
            self.appendSource( d.SOURCE )
            self.appendGlobSource( d.GLOBSOURCE )
            self.appendCompilerFlag( d.CFLAG )
            self.appendLinkFlag( d.CFLAG )


# STM32F10x
class Stm32f1(Stm32):
    def __init__(self):
        Stm32.__init__( self, drivers=[
            STM32F10X_StartupDriver(self.density),
            STM32F10X_StdPeripheralDriver() ] )

class Stm32f1xld(Stm32):
    density = 'ld'
                
class Stm32f1xldvl(Stm32f1):
    density = 'ld_vl'
 
class Stm32f1md(Stm32f1):
    density = 'md'

class Stm32f1mdvl(Stm32f1):
    density = 'md_vl'

class Stm32f1hd(Stm32f1):
    density = 'hd'

class Stm32f1hdvl(Stm32f1):
    density = 'hd_vl'

# STM32L1xx
class Stm32l1(Stm32):
    def __init__(self):
        Stm32.__init__( self, drivers=[
            STM32L1XX_StartupDriver(self.density),
            STM32L1XX_StdPeripheralDriver() ] )

class Stm32l1md(Stm32l1):
    density = 'md'

class Stm32l1mdp(Stm32l1):
    density = 'mdp'

class Stm32l1hd(Stm32l1):
    density = 'hd'

# STM32F2xx
class Stm32f2(Stm32):
    def __init__(self):
         Stm32.__init__( self, drivers=[
            STM32F2XX_StartupDriver(),
            STM32F2XX_StdPeripheralDriver() ] )


