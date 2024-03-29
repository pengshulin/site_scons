'''ST STM32 Series'''
# MCUSH Scons Build Scripts, designed by Peng Shulin 
from Cortex import CortexM0, CortexM3, CortexM4, CortexM7
from Cortex import CMSIS_DSP_Driver
from VEnvironment import Driver, hal_config


# Startup driver
class STM32F0XX_StartupDriver(Driver):
    PATH = ['/CMSIS/Device/ST/STM32F0xx/Include']
    EX_DEF = {
        'STM32F030': 'STM32F030',
        'STM32F031': 'STM32F031',
        'STM32F042': 'STM32F042',
        'STM32F051': 'STM32F051',
        'STM32F072': 'STM32F072',
        }

    def __init__(self, cpu):
        self.SOURCE = [
            '/CMSIS/Device/ST/STM32F0xx/Source/Templates/gcc_ride7/startup_%s.s'% cpu.lower(), 
            '/CMSIS/Device/ST/STM32F0xx/Source/Templates/system_stm32f0xx.c' ]
        self.CFLAG = []
        self.CFLAG.append( '-D%s'% cpu )
        if cpu in self.EX_DEF.keys():
            self.CFLAG.append( '-D%s'% self.EX_DEF[cpu] )
        self.LDFLAG = ['-Wl,--entry=Reset_Handler'] 

class STM32F10X_StartupDriver(Driver):
    PATH = ['/CMSIS/Device/ST/STM32F10x/Include']
    def __init__(self, density, include_system=True):
        assert density in ['ld', 'ld_vl', 'md', 'md_vl', 'hd', 'hd_vl', 'xl', 'cl']
        self.SOURCE = [ '/CMSIS/Device/ST/STM32F10x/Source/Templates/gcc_ride7/startup_stm32f10x_%s.s'% density ]
        if include_system:
            self.SOURCE.append( '/CMSIS/Device/ST/STM32F10x/Source/Templates/system_stm32f10x.c' )
        self.CFLAG = ['-DSTM32F10X_%s'% density.upper()]
        self.LDFLAG = ['-Wl,--entry=Reset_Handler'] 

class STM32F1XX_StartupDriver(Driver):
    PATH = ['/CMSIS/Device/ST/STM32F1xx/Include']
    def __init__(self, cpu_group):
        assert cpu_group in [
            'STM32F100xB', 'STM32F100xE', 'STM32F101x6', 'STM32F101xB',
            'STM32F101xE', 'STM32F101xG', 'STM32F102x6', 'STM32F102xB',
            'STM32F103x6', 'STM32F103xB', 'STM32F103xE', 'STM32F103xG',
            'STM32F105xC', 'STM32F107xC' ]
        self.SOURCE = [
            '/CMSIS/Device/ST/STM32F1xx/Source/Templates/gcc/startup_%s.s'% cpu_group.lower(), 
            '/CMSIS/Device/ST/STM32F1xx/Source/Templates/system_stm32f1xx.c' ]
        self.CFLAG = ['-D%s'% cpu_group]
        self.LDFLAG = ['-Wl,--entry=Reset_Handler'] 


class STM32L1XX_StartupDriver(Driver):
    PATH = ['/CMSIS/Device/ST/STM32L1xx/Include']
    def __init__(self, density):
        assert density in ['md', 'mdp', 'hd']
        self.SOURCE = [
            '/CMSIS/Device/ST/STM32L1xx/Source/Templates/gcc_ride7/startup_stm32l1xx_%s.s'% density, 
            '/CMSIS/Device/ST/STM32L1xx/Source/Templates/system_stm32l1xx.c' ]
        self.CFLAG = ['-DSTM32L1XX_%s'% density.upper()]
        self.LDFLAG = ['-Wl,--entry=Reset_Handler'] 

class STM32F2XX_StartupDriver(Driver):
    PATH = ['/CMSIS/Device/ST/STM32F2xx/Include']
    def __init__(self):
        self.SOURCE = [
            '/CMSIS/Device/ST/STM32F2xx/Source/Templates/gcc_ride7/startup_stm32f2xx.s', 
            '/CMSIS/Device/ST/STM32F2xx/Source/Templates/system_stm32f2xx.c' ]
        self.CFLAG = []
        self.LDFLAG = ['-Wl,--entry=Reset_Handler'] 

class STM32F4XX_LegacyStartupDriver(Driver):
    PATH = ['/CMSIS/Device/ST/STM32F4xx_legacy/Include']
    def __init__(self, cpu_group):
        self.SOURCE = [
            '/CMSIS/Device/ST/STM32F4xx_legacy/Source/Templates/gcc_ride7/startup_%s.s'% cpu_group.lower(), 
            '/CMSIS/Device/ST/STM32F4xx_legacy/Source/Templates/system_stm32f4xx.c' ]
        self.CFLAG = []
        self.CFLAG.append( '-D%s'% cpu_group )
        self.LDFLAG = ['-Wl,--entry=Reset_Handler'] 

class STM32F4XX_StartupDriver(Driver):
    PATH = ['/CMSIS/Device/ST/STM32F4xx/Include']
    def __init__(self, cpu):
        self.SOURCE = [
            '/CMSIS/Device/ST/STM32F4xx/Source/Templates/gcc/startup_%s.s'% cpu.lower(), 
            '/CMSIS/Device/ST/STM32F4xx/Source/Templates/system_stm32f4xx.c' ]
        self.CFLAG = []
        self.CFLAG.append( '-D%s'% cpu )
        self.LDFLAG = ['-Wl,--entry=Reset_Handler'] 

class STM32F7XX_StartupDriver(Driver):
    PATH = ['/CMSIS/Device/ST/STM32F7xx/Include']
    def __init__(self, cpu):
        self.SOURCE = [
            '/CMSIS/Device/ST/STM32F7xx/Source/Templates/gcc/startup_%s.s'% cpu.lower(), 
            '/CMSIS/Device/ST/STM32F7xx/Source/Templates/system_stm32f7xx.c' ]
        self.CFLAG = []
        self.CFLAG.append( '-D%s'% cpu )
        self.LDFLAG = ['-Wl,--entry=Reset_Handler'] 

class STM32G0XX_StartupDriver(Driver):
    PATH = ['/CMSIS/Device/ST/STM32G0xx/Include']
    EX_DEF = {
        'STM32G0B0xx': 'STM32G0B0xx',
        'STM32G0B1xx': 'STM32G0B1xx',
        'STM32G0C1xx': 'STM32G0C1xx',
        'STM32G070xx': 'STM32G070xx',
        'STM32G071xx': 'STM32G071xx',
        'STM32G081xx': 'STM32G081xx',
        'STM32G050xx': 'STM32G050xx',
        'STM32G051xx': 'STM32G051xx',
        'STM32G061xx': 'STM32G061xx',
        'STM32G030xx': 'STM32G030xx',
        'STM32G031xx': 'STM32G031xx',
        'STM32G041xx': 'STM32G041xx',
        }

    def __init__(self, cpu):
        self.SOURCE = [
            '/CMSIS/Device/ST/STM32G0xx/Source/Templates/gcc/startup_%s.s'% cpu.lower(), 
            '/CMSIS/Device/ST/STM32G0xx/Source/Templates/system_stm32g0xx.c' ]
        self.CFLAG = []
        self.CFLAG.append( '-D%s'% cpu )
        if cpu in self.EX_DEF.keys():
            self.CFLAG.append( '-D%s'% self.EX_DEF[cpu] )
        self.LDFLAG = ['-Wl,--entry=Reset_Handler'] 


# Standard Peripheral driver
class STM32F0XX_StdPeripheralDriver(Driver):
    PATH = ['/ST/STM32F0xx_StdPeriph_Driver/inc']
    GLOBSOURCE = ['/ST/STM32F0xx_StdPeriph_Driver/src/*.c']
    CFLAG = ['-DUSE_STDPERIPH_DRIVER']

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

class STM32F4XX_StdPeripheralDriver(Driver):
    PATH = ['/ST/STM32F4xx_StdPeriph_Driver/inc']
    GLOBSOURCE = ['/ST/STM32F4xx_StdPeriph_Driver/src/*.c']
    CFLAG = ['-DUSE_STDPERIPH_DRIVER']


# HAL/LL Driver
class STM32F1XX_HAL_Driver(Driver):
    PATH = ['/ST/STM32F1xx_HAL_Driver/Inc']
    GLOBSOURCE = ['/ST/STM32F1xx_HAL_Driver/Src/stm32f1xx_*.c']
    GLOBSOURCE_EX = ['/ST/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_*template.c']
    CFLAG = ['-DUSE_HAL_DRIVER', '-DUSE_FULL_LL_DRIVER']

class STM32F4XX_HAL_Driver(Driver):
    PATH = ['/ST/STM32F4xx_HAL_Driver/Inc']
    GLOBSOURCE = ['/ST/STM32F4xx_HAL_Driver/Src/stm32f4xx_*.c']
    GLOBSOURCE_EX = ['/ST/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_*template.c']
    CFLAG = ['-DUSE_HAL_DRIVER', '-DUSE_FULL_LL_DRIVER']

class STM32F7XX_HAL_Driver(Driver):
    PATH = ['/ST/STM32F7xx_HAL_Driver/Inc']
    GLOBSOURCE = ['/ST/STM32F7xx_HAL_Driver/Src/stm32f7xx_*.c']
    GLOBSOURCE_EX = ['/ST/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_*template.c']
    CFLAG = ['-DUSE_HAL_DRIVER', '-DUSE_FULL_LL_DRIVER']

class STM32G0XX_HAL_Driver(Driver):
    PATH = ['/ST/STM32G0xx_HAL_Driver/Inc']
    GLOBSOURCE = ['/ST/STM32G0xx_HAL_Driver/Src/stm32g0xx_*.c']
    GLOBSOURCE_EX = ['/ST/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_*template.c']
    CFLAG = ['-DUSE_HAL_DRIVER', '-DUSE_FULL_LL_DRIVER']


# LL-only Driver
class STM32F1XX_LL_Driver(Driver):
    PATH = ['/ST/STM32F1xx_HAL_Driver/Inc']
    GLOBSOURCE = ['/ST/STM32F1xx_HAL_Driver/Src/stm32f1xx_ll*.c',
                  '/ST/STM32F1xx_HAL_Driver/Src/stm32f1xx_hal_cortex.c',
                  ]
    CFLAG = ['-DUSE_FULL_LL_DRIVER']

class STM32F4XX_LL_Driver(Driver):
    PATH = ['/ST/STM32F4xx_HAL_Driver/Inc']
    GLOBSOURCE = ['/ST/STM32F4xx_HAL_Driver/Src/stm32f4xx_ll*.c',
                  '/ST/STM32F4xx_HAL_Driver/Src/stm32f4xx_hal_cortex.c',
                 ]
    CFLAG = ['-DUSE_FULL_LL_DRIVER']

class STM32F7XX_LL_Driver(Driver):
    PATH = ['/ST/STM32F7xx_HAL_Driver/Inc']
    GLOBSOURCE = ['/ST/STM32F7xx_HAL_Driver/Src/stm32f7xx_ll_*.c',
                  '/ST/STM32F7xx_HAL_Driver/Src/stm32f7xx_hal_cortex.c', 
                 ]
    CFLAG = ['-DUSE_FULL_LL_DRIVER']

class STM32G0XX_LL_Driver(Driver):
    PATH = ['/ST/STM32G0xx_HAL_Driver/Inc']
    GLOBSOURCE = ['/ST/STM32G0xx_HAL_Driver/Src/stm32g0xx_ll*.c',
                  '/ST/STM32G0xx_HAL_Driver/Src/stm32g0xx_hal_cortex.c',
                  ]
    CFLAG = ['-DUSE_FULL_LL_DRIVER']



# USB Full Speed driver
class STM32_USB_FS_Driver(Driver):
    PATH = ['/ST/STM32_USB-FS-Device_Driver/inc']
    GLOBSOURCE = ['/ST/STM32_USB-FS-Device_Driver/src/*.c']


# USB device driver
class STM32_USB_DEVICE_Driver(Driver):
    PATH = ['/ST/STM32_USB_Device_Library/Core/Inc']
    GLOBSOURCE = ['/ST/STM32_USB_Device_Library/Core/Src/usbd_*.c']
    GLOBSOURCE_EX = ['/ST/STM32_USB_Device_Library/Core/Src/usbd_*template.c']
    def __init__(self, dev_class=None):
        if dev_class is None:
            try:
                dev_class = self.CLASS
            except:
                pass
        if dev_class is not None:
            self.PATH.append('/ST/STM32_USB_Device_Library/Class/%s/Inc'% dev_class)
            self.SOURCE.append('/ST/STM32_USB_Device_Library/Class/%s/Src/usbd_%s.c'% (dev_class, dev_class.lower()) )

class STM32_USB_DEVICE_AUDIO_Driver(STM32_USB_DEVICE_Driver):
    CLASS = 'AUDIO'

class STM32_USB_DEVICE_CDC_Driver(STM32_USB_DEVICE_Driver):
    CLASS = 'CDC'

class STM32_USB_DEVICE_CustomHID_Driver(STM32_USB_DEVICE_Driver):
    CLASS = 'CustomHID'

class STM32_USB_DEVICE_DFU_Driver(STM32_USB_DEVICE_Driver):
    CLASS = 'DFU'

class STM32_USB_DEVICE_HID_Driver(STM32_USB_DEVICE_Driver):
    CLASS = 'HID'

class STM32_USB_DEVICE_MSC_Driver(STM32_USB_DEVICE_Driver):
    CLASS = 'MSC'


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
# NOTE: symbolic link libSTemWin_CMX_GCC.a needs to be created manually
class STemWin(Driver):
    PATH = ['/ST/STemWin/inc']
    LIBPATH = ['/ST/STemWin/Lib']
    def __init__(self, cortex='CM4', os=True ):
        if os:
            l = 'STemWin_%s_OS_GCC'% cortex
        else:
            l = 'STemWin_%s_GCC'% cortex
        self.LIB.append(l)



    

#############################################################################
# CHIPS BELOW
#############################################################################

class Stm32M0(CortexM0):
    def __init__( self, drivers=None ):
        CortexM0.__init__( self )
        self.appendDrivers( drivers )

class Stm32M3(CortexM3):
    def __init__( self, drivers=None ):
        CortexM3.__init__( self )
        self.appendDrivers( drivers )

class Stm32M4(CortexM4):
    def __init__( self, drivers=None ):
        CortexM4.__init__( self )
        self.appendDrivers( drivers )

class Stm32M7(CortexM7):
    def __init__( self, drivers=None ):
        CortexM7.__init__( self )
        self.appendDrivers( drivers )


# STM32F0xx
class Stm32f0(Stm32M0):
    def __init__(self):
        Stm32M0.__init__( self, drivers=[
            STM32F0XX_StartupDriver(self.cpu),
            STM32F0XX_StdPeripheralDriver() ] )

class Stm32f030xx(Stm32f0):
    cpu = 'STM32F030'

class Stm32f042xx(Stm32f0):
    cpu = 'STM32F042'


# STM32F10x
class Stm32f1(Stm32M3):
    def __init__(self, use_hal_driver=False):
        if use_hal_driver:
            drivers = [ STM32F1XX_StartupDriver(self.cpu_group),
                        STM32F1XX_HAL_Driver() ]
        else:
            drivers = [ STM32F10X_StartupDriver(self.density),
                        STM32F10X_StdPeripheralDriver() ]
        Stm32M3.__init__( self, drivers=drivers )

# - Low-density devices are STM32F101xx, STM32F102xx and STM32F103xx microcontrollers
#   where the Flash memory density ranges between 16 and 32 Kbytes.
# - Low-density value line devices are STM32F100xx microcontrollers where the Flash
#   memory density ranges between 16 and 32 Kbytes.
# - Medium-density devices are STM32F101xx, STM32F102xx and STM32F103xx microcontrollers
#   where the Flash memory density ranges between 64 and 128 Kbytes.
# - Medium-density value line devices are STM32F100xx microcontrollers where the 
#   Flash memory density ranges between 64 and 128 Kbytes.   
# - High-density devices are STM32F101xx and STM32F103xx microcontrollers where
#   the Flash memory density ranges between 256 and 512 Kbytes.
# - High-density value line devices are STM32F100xx microcontrollers where the 
#   Flash memory density ranges between 256 and 512 Kbytes.   
# - XL-density devices are STM32F101xx and STM32F103xx microcontrollers where
#   the Flash memory density ranges between 512 and 1024 Kbytes.
# - Connectivity line devices are STM32F105xx and STM32F107xx microcontrollers.
class Stm32f1ld(Stm32f1):
    density = 'ld'
class Stm32f1ldvl(Stm32f1):
    density = 'ld_vl'
class Stm32f1md(Stm32f1):
    density = 'md'
class Stm32f1mdvl(Stm32f1):
    density = 'md_vl'
class Stm32f1hd(Stm32f1):
    density = 'hd'
class Stm32f1hdvl(Stm32f1):
    density = 'hd_vl'
class Stm32f1xl(Stm32f1):
    density = 'xl'
class Stm32f1cl(Stm32f1):
    density = 'cl'
 
# chips
class Stm32f103x4(Stm32f1ld):
    cpu_group = 'STM32F103x4'
class Stm32f103x6(Stm32f1ld):
    cpu_group = 'STM32F103x6'
class Stm32f103x8(Stm32f1md):
    cpu_group = 'STM32F103x8'
class Stm32f103xb(Stm32f1md):
    cpu_group = 'STM32F103xB'
class Stm32f103xc(Stm32f1hd):
    cpu_group = 'STM32F103xC'
class Stm32f103xd(Stm32f1hd):
    cpu_group = 'STM32F103xD'
class Stm32f103xe(Stm32f1hd):
    cpu_group = 'STM32F103xE'
class Stm32f103xf(Stm32f1xl):
    cpu_group = 'STM32F103xF'
class Stm32f103xg(Stm32f1xl):
    cpu_group = 'STM32F103xG'
class Stm32f105xx(Stm32f1cl):
    cpu_group = 'STM32F105xx'
class Stm32f107xx(Stm32f1cl):
    cpu_group = 'STM32F107xx'
 
 
# STM32L1xx
class Stm32l1(Stm32M3):
    def __init__(self):
        Stm32M3.__init__( self, drivers=[
            STM32L1XX_StartupDriver(self.density),
            STM32L1XX_StdPeripheralDriver() ] )

class Stm32l1md(Stm32l1):
    density = 'md'

class Stm32l1mdp(Stm32l1):
    density = 'mdp'

class Stm32l1hd(Stm32l1):
    density = 'hd'

class Stm32l1xl(Stm32l1):
    density = 'xl'


# STM32F2xx
class Stm32f2(Stm32M3):
    def __init__(self, use_hal_driver=False):
        if use_hal_driver:
            drivers = [ STM32F2XX_StartupDriver(),
                        STM32F2XX_HAL_Driver() ]
        else:
            drivers = [ STM32F2XX_StartupDriver(),
                        STM32F2XX_StdPeripheralDriver() ]
        Stm32M3.__init__( self, drivers=drivers )



# STM32F4xx
class Stm32f4(Stm32M4):
    def __init__(self, use_hal_driver=False):
        if use_hal_driver:
            drivers = [ STM32F4XX_StartupDriver(self.cpu),
                        STM32F4XX_HAL_Driver() ]
        else:
            drivers = [ STM32F4XX_LegacyStartupDriver(self.cpu_group),
                        STM32F4XX_StdPeripheralDriver() ]
        Stm32M4.__init__( self, drivers=drivers )


class Stm32f401xc(Stm32f4):
    cpu = 'STM32F401xC'
    cpu_group = 'STM32F40_41xxx'

class Stm32f401xe(Stm32f4):
    cpu = 'STM32F401xE'
    cpu_group = 'STM32F40_41xxx'

class Stm32f411xe(Stm32f4):
    cpu = 'STM32F411xE'
    cpu_group = 'STM32F40_41xxx'

class Stm32f412rx(Stm32f4):
    cpu = 'STM32F412Rx'
    cpu_group = 'STM32F40_41xxx'

class Stm32f407xx(Stm32f4):
    cpu = 'STM32F407xx'
    cpu_group = 'STM32F40_41xxx'

class Stm32f429xx(Stm32f4):
    cpu = 'STM32F429xx'
    cpu_group = 'STM32F429_439xx'


# STM32F7xx
class Stm32f7(Stm32M7):
    def __init__(self):
        drivers = [ STM32F7XX_StartupDriver(self.cpu),
                        STM32F7XX_HAL_Driver() ]
        Stm32M7.__init__( self, drivers=drivers )


class Stm32f767xx(Stm32f7):
    cpu = 'STM32F767xx'


# STM32G0xx
class Stm32g0(Stm32M0):
    def __init__(self):
        Stm32M0.__init__( self, drivers=[
            STM32G0XX_StartupDriver(self.cpu),
            STM32G0XX_HAL_Driver() ] )

class Stm32g030xx(Stm32g0):
    cpu = 'STM32G030xx'


