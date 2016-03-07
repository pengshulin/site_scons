'''stm32 series'''
from Cortex import CortexM3

class Stm32(CortexM3):
    '''stm32 base class'''
    def __init__( self ):
        CortexM3.__init__( self )
        self.appendCompilerFlag( ['-DUSE_STDPERIPH_DRIVER'] )
        self.appendLinkFlag( ['--entry', 'Reset_Handler'] )
    

class Stm32f1(Stm32):
    def __init__( self,  density='md' ):
        Stm32.__init__( self )
        self.appendPath( ['/CMSIS/Device/ST/STM32F10x/Include',
                          '/ST/STM32F10x_StdPeriph_Driver/inc',
                          '/ST/STM32_USB-FS-Device_Driver/inc', ] )
        self.appendCompilerFlag( ['-DSTM32F10X_%s'% density.upper()] )
        self.appendSource( ['/CMSIS/Device/ST/STM32F10x/Source/Templates/gcc_ride7/startup_stm32f10x_%s.s'% density.lower()] )
        self.appendGlobSource( '/ST/STM32F10x_StdPeriph_Driver/src/*.c' )

class Stm32f1xld(Stm32f1):
    def __init__( self ):
        Stm32f1.__init__( self, density='ld' )

class Stm32f1xldvl(Stm32f1):
    def __init__( self ):
        Stm32f1.__init__( self, density='ld_vl' )

class Stm32f1md(Stm32f1):
    def __init__( self ):
        Stm32f1.__init__( self, density='md' )

class Stm32f1mdvl(Stm32f1):
    def __init__( self ):
        Stm32f1.__init__( self, density='md_vl' )

class Stm32f1hd(Stm32f1):
    def __init__( self ):
        Stm32f1.__init__( self, density='hd' )

class Stm32f1hdvl(Stm32f1):
    def __init__( self ):
        Stm32f1.__init__( self, density='hd_vl' )

class Stm32f1xl(Stm32f1):
    def __init__( self ):
        Stm32f1.__init__( self, density='xl' )

class Stm32f1cl(Stm32f1):
    def __init__( self ):
        Stm32f1.__init__( self, density='cl' )

class Stm32f2(Stm32):
    def __init__( self ):
        Stm32.__init__( self )
        self.appendPath( ['/CMSIS/Device/ST/STM32F2xx/Include',
                          '/ST/STM32F2xx_StdPeriph_Driver/inc',
                          '/ST/STM32_USB-FS-Device_Driver/inc', ] )
        self.appendSource( ['/CMSIS/Device/ST/STM32F2xx/Source/Templates/gcc_ride7/startup_stm32f2xx.s'] )
        self.appendGlobSource( '/ST/STM32F2xx_StdPeriph_Driver/src/*.c' )

class Stm32l1(Stm32):
    def __init__( self,  density='md' ):
        Stm32.__init__( self )
        self.appendPath( ['/CMSIS/Device/ST/STM32L1xx/Include',
                          '/ST/STM32L1xx_StdPeriph_Driver/inc',
                          '/ST/STM32_USB-FS-Device_Driver/inc',
                          '/ST/STMTouch_Driver/inc',
                          '/ST/STMTouch_Driver/inc/to adapt', ] )
        self.appendCompilerFlag( ['-DSTM32L1XX_%s'% density.upper()] )
        self.appendSource( ['/CMSIS/Device/ST/STM32L1xx/Source/Templates/gcc_ride7/startup_stm32l1xx_%s.s'% density.lower()] )
        self.appendGlobSource( '/ST/STM32L1xx_StdPeriph_Driver/src/*.c' )
 
 
class Stm32l1md(Stm32l1):
    def __init__( self ):
        Stm32l1.__init__( self, density='md' )

class Stm32l1mdp(Stm32l1):
    def __init__( self ):
        Stm32l1.__init__( self, density='mdp' )

class Stm32l1hd(Stm32l1):
    def __init__( self ):
        Stm32l1.__init__( self, density='hd' )


