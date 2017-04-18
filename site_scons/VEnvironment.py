'''Virtual Environment'''
from SCons.Builder import Builder
from SCons.Environment import Environment
from SCons.Errors import StopError

from Toolchain import Gcc

from os import environ, getenv, getcwd
from os.path import basename, abspath, isfile, join, splitext, dirname
from fnmatch import fnmatch 


_SWITCH_CONFIRM = ['1', 'Y', 'y', 'T', 't']

def _getBoolEnv( name ):
    return bool( getenv(name) in _SWITCH_CONFIRM )


class VEnvironment(Environment):
    source = []
    root = None
    linkfile = None

    _TOOLCHAIN = Gcc

    # default flags
    _DEF_CCFLAGS = ['-Wno-unused-but-set-variable', '-Wall']
    _DEF_CPPPATH = []
    _DEF_LIBPATH = []
    _DEF_LIBS = []
    _DEF_LINKFLAGS = ['-Wl,--gc-sections']

    # additional flags
    _CCFLAGS = []
    _CPPPATH = []
    _LIBPATH = []
    _LIBS = []
    _LINKFLAGS = []


    def _initFromSysEnv( self ):
        self.VERBOSE = _getBoolEnv( 'VERBOSE' )
        self.INFO = _getBoolEnv( 'INFO' )
        self.DEBUG = _getBoolEnv( 'DEBUG' )

    def __init__( self ):
        Environment.__init__( self, ENV=environ )

        self._initFromSysEnv()

        tool = self._TOOLCHAIN()
        self['AR'] = tool.AR
        self['AS'] = tool.AS
        self['CC'] = tool.CC
        self['CXX'] = tool.CXX
        self['LINK'] = tool.LINK
        self['NM'] = tool.NM
        self['RANDLIB'] = tool.RANDLIB
        self['OBJCOPY'] = tool.OBJCOPY
        self['OBJDUMP'] = tool.OBJDUMP

        self.Append( CCFLAGS=self._DEF_CCFLAGS )
        self.Append( CPPPATH=self._DEF_CPPPATH )
        self.Append( LIBS=self._DEF_LIBS )
        self.Append( LIBPATH=self._DEF_LIBPATH )
        self.Append( LINKFLAGS=self._DEF_LINKFLAGS )

        self.Append( CCFLAGS=self._CCFLAGS )
        self.Append( CPPPATH=self._CPPPATH )
        self.Append( LIBS=self._LIBS )
        self.Append( LIBPATH=self._LIBPATH )
        self.Append( LINKFLAGS=self._LINKFLAGS )

        BIN_BUILDER = Builder( action = tool.OBJCOPY + ' -O binary $SOURCE $TARGET', suffix='.bin', src_suffix='.elf' )
        self.Append( BUILDERS={'Bin': BIN_BUILDER} )

        HEX_BUILDER = Builder( action = tool.OBJCOPY + ' -O ihex $SOURCE $TARGET', suffix='.hex', src_suffix='.elf' )
        self.Append( BUILDERS={'Hex': HEX_BUILDER} )
        
        SIZE_BUILDER = Builder( action = tool.SIZE + ' -t $SOURCE', src_suffix='.elf' )
        self.Append( BUILDERS={'Size': SIZE_BUILDER} )

        DUMP_BUILDER = Builder( action = tool.OBJDUMP + ' -x -S -D -s $SOURCE $TARGET', suffix='.S', src_suffix='.o' )
        self.Append( BUILDERS={'Dump': DUMP_BUILDER} )

        self.findRoot()

    def appendCompilerFlag( self, flag ):
        assert isinstance(flag, list) 
        self.Append( CCFLAGS=flag )

    def appendLinkFlag( self, flag ):
        assert isinstance(flag, list) 
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
        assert isinstance(path, list) 
        self.Append( CPPPATH=self.applyRoot(path) )

    def appendLibPath( self, path ):
        assert isinstance(path, list) 
        self.Append( LIBPATH=self.applyRoot(path) )
        
    def appendLib( self, lib ):
        assert isinstance(lib, list) 
        self.Append( LIBS=lib )

    def appendSource( self, source ):
        assert isinstance(source, list) 
        for f in self.applyRoot(source):
            if not f in self.source:
                self.source.append(f)

    def _glob( self, pat, exclude_pat=None ):
        assert isinstance(pat, str) 
        if pat.startswith('/') and not pat.startswith(self.root):
            result = self.Glob( join(self.root, pat[1:]) )
        else:
            result = self.Glob( pat )
        #print 'Glob:', pat
        #print [str(f) for f in result]
        if exclude_pat:
            ret = []
            for fil in result:
                if not fnmatch( str(fil), exclude_pat ):
                    ret.append( fil )
            return ret
        else:
            return result

    def appendGlobSource( self, pat, expat=None ):
        assert isinstance(pat, list) 
        p = self.applyRoot(pat)
        if expat is not None:
            assert isinstance(expat, str) 
            expat = self.applyRoot([expat])[0]
        for p in pat:
            self.appendSource( self._glob(p, expat) )

    def findRoot( self ):
        _dir = abspath(getcwd())
        while not isfile(join(_dir,'root')) and not isfile(join(_dir,'ROOT')):
            _dir = abspath( join( _dir, '..' ) )
            if _dir == '/':
                break 
        if _dir != '/':
            self.root = _dir 
        print 'scons: root', self.root
        
    def getName( self ):
        dirname = basename(getcwd())
        if dirname.startswith('app'):
            name = dirname[3:]
        elif dirname.startswith('lib'):
            name = dirname[3:]
        else:
            name = dirname
        return name + '_dbg' if self.DEBUG else name

    def setLinkfile( self, linkfile ):
        '''set link file'''
        if linkfile.startswith('/'):
            self.linkfile = join(self.root, linkfile[1:])
        else:
            self.linkfile = linkfile
         
    def makeApp( self, name=None ):
        '''make application'''
        if self.linkfile:
            self.appendLinkFlag( ['-T%s'% self.linkfile] )
            self.appendLinkFlag( ['-L%s'% dirname(self.linkfile)] )
            
        if not name:
            name = self.getName()
        self.appendLinkFlag( ['-Wl,-Map,%s.map'% name] )
        elffile = self.Program( name + '.elf', self.source )
        binfile = self.Bin( name + '.bin', elffile )
        hexfile = self.Hex( name + '.hex', elffile )
        self.Depends( binfile, elffile )
        self.Depends( hexfile, elffile )
        self.Size( source=elffile )
        # TODO: add obj dumper if needed

    def makeLib( self, name=None ):
        if not name:
            name = self.getName()
        libfile = self.Library( name, self.source )
        self.Size( source=libfile )


    def makeMDPDF( self, fname ):
        try:
            self.builder_pdf
        except AttributeError:
            self.builder_pdf = Builder(action='markdown2pdf $SOURCES $TARGET',
                       suffix='.pdf', src_suffix='.md' )
            self.Append(BUILDERS = {'MDPDF': self.builder_pdf})
        base = splitext(fname)[0]
        self.MDPDF( target='%s.pdf'% base, source='%s.md'% base )


