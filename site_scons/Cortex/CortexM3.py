'''cortex-m3 based controller'''
from SCons.Builder import Builder
from SCons.Environment import Environment
from SCons.Errors import StopError

from Toolchain import ArmNoneEabiGcc

from os import environ, getcwd
from os.path import basename, abspath, isfile, join
from fnmatch import fnmatch 


class CortexM3(Environment):
    '''base class for cortex-m3'''
    source = []
    root = None
    linkfile = None

    _TOOLCHAIN = ArmNoneEabiGcc
    _CCFLAGS = ['-mcpu=cortex-m3' ,'-mthumb', '-Wall' ]
    _CPPPATH = []
    _LIBPATH = []
    _LIBS = []
    _LINKFLAGS = ['-mcpu=cortex-m3', '-mthumb', '-Wl,--gc-sections']

    def __init__( self ):
        Environment.__init__( self, ENV=environ )

        tool = self._TOOLCHAIN()
        self['AR'] = tool.AR
        self['AS'] = tool.AS
        self['CC'] = tool.CC
        self['LINK'] = tool.LINK
        self['NM'] = tool.NM
        self['RANDLIB'] = tool.RANDLIB

        self.Append( CCFLAGS=self._CCFLAGS )
        self.Append( CPPPATH=self._CPPPATH )
        self.Append( LIBS=self._LIBS )
        self.Append( LIBPATH=self._LIBPATH )
        self.Append( LINKFLAGS=self._LINKFLAGS )

        BIN_BUILDER = Builder( action = tool.OBJCOPY + ' -O binary $SOURCE $TARGET' )
        self.Append( BUILDERS={'Bin': BIN_BUILDER} )

        HEX_BUILDER = Builder( action = tool.OBJCOPY + ' -O ihex $SOURCE $TARGET' )
        self.Append( BUILDERS={'Hex': HEX_BUILDER} )

        self.findRoot()
        self.appendPath( ['/CMSIS/Include'] )

    def appendCompilerFlag( self, flag ):
        self.Append( CCFLAGS=flag )

    def appendLinkFlag( self, flag ):
        self.Append( LINKFLAGS=flag )
    
    def applyRoot( self, path ):
        ret = []
        for p in path:
            p = str(p)
            if p.startswith( '/' ) and not p.startswith(self.root):
                ret.append( join(self.root, p[1:]) )
            else:
                ret.append( p )
        return ret

    def appendPath( self, path ):
        self.Append( CPPPATH=self.applyRoot(path) )

    def appendLibPath( self, path ):
        self.Append( LIBPATH=self.applyRoot(path) )
        
    def appendLib( self, lib ):
        self.Append( LIBS=lib )

    def appendSource( self, source ):
        self.source += self.applyRoot(source)

    def appendGlobSource( self, pat, expat=None ):
        self.appendSource( self.glob(pat, expat) )

    def findRoot( self ):
        _dir = abspath(getcwd())
        while not isfile( join( _dir, 'root' ) ):
            _dir = abspath( join( _dir, '..' ) )
            if _dir == '/':
                break 
        if _dir != '/':
            self.root = _dir 
        print 'scons: root', self.root
        
    def getName( self ):
        dirname = basename(getcwd())
        if dirname.startswith('app'):
            return dirname[3:]
        elif dirname.startswith('lib'):
            return dirname[3:]
        else:
            return dirname

    def glob( self, pat, exclude_pat=None ):
        if pat.startswith('/') and not pat.startswith(self.root):
            result = self.Glob( join(self.root, pat[1:]) )
        else:
            result = self.Glob( pat )
        if exclude_pat:
            ret = []
            for fil in ret:
                if not fnmatch( str(fil), exclude_pat ):
                    ret.append( fil )
            return ret
        else:
            return result

    def setLinkfile( self, linkfile ):
        '''set link file'''
        if linkfile.startswith('/'):
            self.linkfile = join(self.root, linkfile[1:])
        else:
            self.linkfile = linkfile
         
    def makeApp( self ):
        '''make application'''
        if self.linkfile is None:
            StopError( 'no link file assigned' )
        self.appendLinkFlag( ['-T%s'% self.linkfile] )
        name = self.getName()
        self.appendLinkFlag( ['-Wl,-Map,%s.map'% name] )
        elffile = self.Program( name + '.elf', self.source )
        binfile = self.Bin( name + '.bin', elffile )
        hexfile = self.Hex( name + '.hex', elffile )
        self.Depends( binfile, elffile )
        self.Depends( hexfile, elffile )

    def makeLib( self ):
        self.Library( self.getName(), self.source )

