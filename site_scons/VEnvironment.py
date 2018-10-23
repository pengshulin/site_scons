'''Virtual Environment'''
# mcu build scripts based on scons, designed by PengShulin 
# Peng Shulin <trees_peng@163.com> 2018
from SCons.Builder import Builder
from SCons.Action import Action
from SCons.Environment import Environment
from SCons.Errors import StopError

from Toolchain import Gcc

from os import environ, getenv, getcwd, system
from os.path import basename, abspath, isfile, join, splitext, dirname
from fnmatch import fnmatchcase
from time import strftime
from sys import path as sys_path
import sys
from subprocess import check_output

_SWITCH_CONFIRM = ['1', 'Y', 'y', 'T', 't', 'yes', 'Yes', 'YES', 'true', 'True', 'TRUE']

def getBoolEnv( name ):
    return bool( getenv(name) in _SWITCH_CONFIRM )

def _findRoot(relative=False):
    _dir = abspath(getcwd())
    _dir2 = ''
    while not isfile(join(_dir,'root')) and not isfile(join(_dir,'ROOT')):
        _dir = abspath( join( _dir, '..' ) )
        _dir2 = join( _dir2, '..' )
        if _dir == '/':
            break 
    return None if _dir == '/' else (_dir2 if relative else _dir)

class Driver():
    PATH = []
    SOURCE = []
    GLOBSOURCE = []
    GLOBSOURCE_EX = None
    CFLAG = []
    LIBPATH = []
    LIB = []
    LDFLAG = []

class VEnvironment(Environment):
    source = []
    root = None
    linkfile = None

    _TOOLCHAIN = Gcc

    # default flags
    _DEF_CCFLAGS = ['-Wno-unused-but-set-variable', '-Wall',
                    #'-pedantic',
                    '-ffunction-sections', '-fdata-sections']
    _DEF_CPPPATH = []
    _DEF_LIBPATH = []
    _DEF_LIBS = ['m']
    _DEF_LINKFLAGS = ['-Wl,--gc-sections']

    # additional flags
    _CCFLAGS = []
    _CPPPATH = []
    _LIBPATH = []
    _LIBS = []
    _LINKFLAGS = []
    # NOTE: load sequence:
    # 1. load ~/.splintrc
    # 2. override by ./.splintrc
    # 3. override by command line args
    _LINTFLAGS = [
        '-linelen 1000',  # all message in one line
        '+quiet',
        '-D__GNUC__=4',
        '-D__builtin_va_list=int',
        ]

    def _initFromSysEnv( self ):
        self.VERBOSE = getBoolEnv( 'VERBOSE' )
        self.INFO = getBoolEnv( 'INFO' )
        self.DEBUG = getBoolEnv( 'DEBUG' )
        self.LINT = getBoolEnv( 'LINT' )
        self.LINT_FILE = getBoolEnv( 'LINT_FILE' )
        self.NO_PARALLEL = getBoolEnv( 'NO_PARALLEL' )

    def getEnv( self, name ):
        return getenv(name, '')

    def getBoolEnv( self, name ):
        return getBoolEnv( name )
    
    def _initBuildDate( self ):
        self.BUILD_DATE = strftime("%y-%m-%d %H:%M:%S")

    def __init__( self ):
        Environment.__init__( self, ENV=environ )

        self._initFromSysEnv()
        self._initBuildDate()

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
        if self._LIBS:
            self.Append( LIBS=self._LIBS )
        self.Append( LIBPATH=self._LIBPATH )
        self.Append( LINKFLAGS=self._LINKFLAGS )

        BIN_BUILDER = Builder( action = tool.OBJCOPY + ' -O binary $SOURCE $TARGET', suffix='.bin', src_suffix='.elf' )
        self.Append( BUILDERS={'Bin': BIN_BUILDER} )

        HEX_BUILDER = Builder( action = tool.OBJCOPY + ' -O ihex $SOURCE $TARGET', suffix='.hex', src_suffix='.elf' )
        self.Append( BUILDERS={'Hex': HEX_BUILDER} )
        
        SIZE_BUILDER = Builder( action = tool.SIZE + ' -t $SOURCE', src_suffix='.elf' )
        self.Append( BUILDERS={'Size': SIZE_BUILDER} )

        DUMP_BUILDER = Builder( action = tool.OBJDUMP + ' -adhlS $SOURCE > $TARGET', suffix='.lst', src_suffix='.elf' )
        self.Append( BUILDERS={'Dump': DUMP_BUILDER} )
        
        #MAP_BUILDER = Builder( action = 'touch $TARGET', suffix='.map', src_suffix='.elf' )
        #self.Append( BUILDERS={'Map': MAP_BUILDER} )

        self.findRoot()
        if not self.NO_PARALLEL:
            self.setMultiJobs()

    def setMultiJobs(self):
        cpus = 0
        try:
            for l in open('/proc/cpuinfo','r').readlines():
                if l.startswith('processor'):
                    cpus += 1
        except:
            pass
        if cpus > 1:
            #print( 'scons: cpu number %d'% cpus )
            self.SetOption('num_jobs', cpus)

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
        #print 'applyRoot', ret
        return ret

    def appendPath( self, path ):
        if path:
            assert isinstance(path, list) 
            self.Append( CPPPATH=self.applyRoot(path) )
    
    def appendLibPath( self, path ):
        if path:
            assert isinstance(path, list) 
            self.Append( LIBPATH=self.applyRoot(path) )
        
    def appendLib( self, lib ):
        if lib:
            assert isinstance(lib, list)
            for l in lib:
                assert l != 'lib'
            self.Append( LIBS=lib )

    def appendSource( self, source ):
        assert isinstance(source, list) 
        #print 'appendSource', source
        for f in self.applyRoot(source):
        #for f in source:
            if not f in self.source:
                self.source.append(f)
                #print 'appended', f

    def _glob( self, pat, exclude_pat=None ):
        assert isinstance(pat, str) 
        if pat.startswith('/') and not pat.startswith(self.root):
            result = self.Glob( join(self.root, pat[1:]) )
        else:
            result = self.Glob( pat )
        #print 'Glob:', pat, [str(f) for f in result], exclude_pat
        if exclude_pat:
            #print 'Expat:', exclude_pat
            ret = []
            for fil in result:
                fname = unicode(fil)
                match = False
                for p in exclude_pat:
                    if fnmatchcase( fname, p ):
                        match = True
                        break
                if not match:
                    ret.append( fil )
            #print 'Glob filtered:', [str(f) for f in ret],
            return ret
        else:
            return result

    def appendGlobSource( self, pat, expat=None ):
        assert isinstance(pat, list) 
        p = self.applyRoot(pat)
        if expat is not None:
            #print type(expat), expat
            assert isinstance(expat, list) 
            expat = self.applyRoot(expat)
        for p in pat:
            self.appendSource( self._glob(p, expat) )

    def findRoot( self ):
        self.root = _findRoot()
        print( 'scons: root ' + self.root )
        
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

    def appendLintFlag( self, flags ):
        self._LINTFLAGS.append( flags )

    def prepareLintEnv( self ):
        try:
            self.lint_env_inited
            return
        except AttributeError:
            pass
        cmd = 'splint'
        #p = check_output( ['arm-none-eabi-gcc', '-print-libgcc-file-name'] )
        #cmd += ' -I' + join(dirname(p), 'include')
        cmd += ' -I/usr/include/newlib'
        for d in self['CCFLAGS']:
            if d.startswith('-D'):
                cmd += ' ' + d
        for i in self['CPPPATH']:
            if i.find(' ') == -1:
                cmd += ' -I' + i
            else:
                cmd += ' -I"' + i + '"'
        for f in self._LINTFLAGS:
            cmd += ' ' + f

        if self.LINT_FILE:
            cmd2 = cmd + ' $SOURCE > $TARGET'
        else:
            cmd2 = cmd + ' $SOURCE'
        #print 'lint cmd', cmd
        #SPLINT_CHECKER = Builder( action=cmd2, suffix='.lint', src_suffix='.c' )
        #self.Append( BUILDERS={'SPLint': SPLINT_CHECKER} )
        self.splint_cmd = Action(cmd2)

        self.lint_env_inited = True

    #def makeLintCheck( self ):
    #    self.prepareLintEnv()
    #    for sfile in self.source:
    #        a, b = splitext(str(sfile))
    #        if b != '.c':
    #            continue
    #        lint = self.SPLint( a+'.lint', sfile )
    #        self.Depends( lint, sfile )
    #        #print lint, sfile
    #        #cmd3 = cmd + ' ' + sfile + ' > ' + a+'.lint'
    #        #cmd3 = cmd + ' ' + sfile
    #        #print cmd3
    #        #system( cmd3 )
    #        #l = Action( cmd3 )
    #        #self.Depends( l, sfile )
    #        #self.lint_list.append( l )

    def makeApp( self, name=None ):
        '''make application'''
        self.prepareLintEnv()
        try:
            self._optimize_flags_added
        except AttributeError:
            self.appendOptimizeFlags()
        if self.linkfile:
            linkfile_dir = dirname(self.linkfile)
            if linkfile_dir:
                # linkfile in different directory, append search path
                self.appendLinkFlag( ['-Wl,-L%s'% linkfile_dir] )
            self.appendLinkFlag( ['-Wl,-T%s'% self.linkfile] )
            
        #self.appendCompilerFlag( ['-DBUILD_DATE=%s'% self.BUILD_DATE] )
            
        if not name:
            name = self.getName()
        self.appendLinkFlag( ['-Wl,--Map=%s.map'% name] )
        objs = []
        for sfile in self.source:
            obj = self.Object(sfile)
            objs.append( obj )
            if self.LINT:
                a, b = splitext(str(sfile))
                if b == '.c':
                    #self.AddPreAction(obj, self.splint_cmd)
                    self.AddPostAction(obj, self.splint_cmd)
         
        elffile = self.Program( name + '.elf', objs )
        #elffile = self.Program( name + '.elf', self.source )
        binfile = self.Bin( name + '.bin', elffile )
        hexfile = self.Hex( name + '.hex', elffile )
        lstfile = self.Dump( name + '.lst', elffile )
        #mapfile = self.Map( name + '.map', elffile )
        self.Depends( binfile, elffile )
        self.Depends( hexfile, elffile )
        self.Depends( lstfile, elffile )
        #self.Depends( mapfile, elffile )
        self.Size( source=elffile )
        # TODO: add obj dumper if needed

    def makeLib( self, name=None ):
        self.prepareLintEnv()
        if not name:
            name = self.getName()
        objs = []
        for sfile in self.source:
            obj = self.Object(sfile)
            objs.append( obj )
            if self.LINT:
                a, b = splitext(str(sfile))
                if b == '.c':
                    self.AddPreAction(obj, self.splint_cmd)
 
        libfile = self.Library( name, objs )
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

    def makeMDLandSlide( self, fname, pdf_mode=False ):
        try:
            self.builder_landslide_html
        except AttributeError:
            self.builder_landslide_html = Builder(action='landslide $SOURCES -d $TARGET',
                       suffix='.html', src_suffix='.md' )
            self.builder_landslide_pdf = Builder(action='landslide $SOURCES -d $TARGET',
                       suffix='.pdf', src_suffix='.md' )
            self.Append(BUILDERS = {'MDLandSlideHTML': self.builder_landslide_html})
            self.Append(BUILDERS = {'MDLandSlidePDF': self.builder_landslide_pdf})
        base = splitext(fname)[0]
        if pdf_mode:
            self.MDLandSlidePDF( target='%s.pdf'% base, source='%s.md'% base )
        else:
            self.MDLandSlideHTML( target='%s.html'% base, source='%s.md'% base )


    def appendOptimizeFlags( self, optimize_flags=None, define_flags=None ):
        if optimize_flags is None:
            if self.DEBUG:
                optimize_flags = ['-g', '-O0']
            else:
                optimize_flags = ['-g', '-O3', '-Werror']
        self.appendCompilerFlag(optimize_flags)
        self._optimize_flags_added = True
        if define_flags is None:
            if self.DEBUG:
                define_flags = ['DEBUG']
            else:
                define_flags = ['NDEBUG']
        self.appendDefineFlags(define_flags)

    def appendDefineFlags( self, define_flags=None ):
        if define_flags is None:
            return
        self.appendCompilerFlag(['-D%s'% d for d in define_flags])

    def appendDriver( self, d ):
        if isinstance(d, Driver):
            self.appendPath( d.PATH )
            self.appendLibPath( d.LIBPATH )
            self.appendLib( d.LIB )
            self.appendSource( d.SOURCE )
            self.appendGlobSource( d.GLOBSOURCE, d.GLOBSOURCE_EX )
            self.appendCompilerFlag( d.CFLAG )
            self.appendLinkFlag( d.LDFLAG )

    def appendDrivers( self, drivers ):
        if drivers:
            for d in drivers: 
                self.appendDriver(d)


    def resetSources( self ):
        self.source = []

    appendPaths = appendPath
    appendGlobSources = appendGlobSource
    appendSources = appendSource
    appendLibPaths = appendLibPath
    appendLibs = appendLib
    appendCompileFlag = appendCompilerFlag
    appendCompileFlags = appendCompilerFlag
    appendCompilerFlags = appendCompilerFlag
    appendLinkFlags = appendLinkFlag
    appendLinkerFlag = appendLinkFlag
    appendLinkerFlags = appendLinkFlag
    appendDefineFlag = appendDefineFlags
    appendDefinedFlag = appendDefineFlags
    appendDefinedFlags = appendDefineFlags

    def appendMcush( self ):
        self.appendPath( ['/mcush'] )
        self.appendGlobSource( ['/mcush/*.c'] )
  
    def appendSpiffs( self ):
        self.appendPath( ['/libspiffs'] )
        self.appendGlobSource( ['/libspiffs/*.c'] )

    def appendFatfs( self ):
        self.appendPath( ['/libFatFs/source'] )
        self.appendGlobSource( ['/libFatFs/source/*.c'] )
   
    def appendFreertos( self, heap=3 ):
        self.appendPath( [
            '/libFreeRTOS',
            '/libFreeRTOS/include',
            '/libFreeRTOS/portable/GCC/%s'% self.freertos_port,
            ] )
        self.appendGlobSource( [
            '/libFreeRTOS/*.c',
            '/libFreeRTOS/portable/MemMang/heap_%d.c'% heap,
            '/libFreeRTOS/portable/GCC/%s/port.c'% self.freertos_port,
            ] )
    
    def appendHal( self, haldir, paths=None, sources=None ):
        self.appendPath( ['/hal%s'% haldir] )
        self.appendGlobSource( ['/hal%s/*.c'% haldir] )
        if paths:
            for p in paths:
                self.appendPath( ['/hal%s/%s'% (haldir, p)] )
        if sources:
            for s in sources:
                self.appendGlobSource( ['/hal%s/%s'% (haldir, s)] )
 
 
haldir = getenv('HALDIR', None) 
    
class config():
    paths = []
    sources = []
    # these configurations are treated as keyword arguments when import halXXX/config.py
    append_mcush = True
    append_hal = True
    append_freertos = True
    use_vfs = True
    use_romfs = True
    use_fcfs = False
    use_spiffs = False
    use_fatfs = False
    use_eth = False

    def __getattr__( self, key ):
        if self.__dict__.has_key( key ):
            return self.__dict__[key]
        else:
            self.__dict__[key] = None  # visit unknown attribute
            return None
    

hal_config = config()

# called from SConstruct
# search in 'halXXXXX' directory for 'config.py'
# the config script must include a basic build environment object 'env'
# if load_(hal/mcush/freertos) switch is set (default), .c/.h codes will be included
def loadHalConfig( haldir, *args, **kwargs ):
    global hal_config
    assert isinstance(haldir, str)
    # check if haldir/root/config.py exists
    if haldir.startswith('hal'):
        haldir = haldir[3:]
    root = _findRoot()
    if root is None:
        raise Exception("ROOT not defined")
    config = join(root, 'hal'+haldir, 'config.py')
    if not isfile(config):
        msg = "config.py not exists in %s"% haldir
        raise Exception(msg)
    # append to path so that config.py can be imported
    sys.path.append(join(root, 'hal'+haldir) )
    # prepare hal_config global variable for import
    for k,v in kwargs.items():
        hal_config.__dict__[k] = v
    # print to console
    if hal_config.__dict__:
        print( 'scons: hal_config %s'% (','.join(['%s=%s'% (str(k),str(v)) for k,v in hal_config.__dict__.items()])) )
    else:
        print( 'scons: hal_config default' )
    # load from config.py
    import config as config
    config.env.haldir = haldir
    # NOTE: hal_config contents may be modified by 'import config'
    # auto load .c/.h sources
    if hal_config.append_hal:
        config.env.appendHal( haldir, hal_config.paths, hal_config.sources )
    if hal_config.append_mcush:
        config.env.appendMcush()
    if hal_config.append_freertos:
        config.env.appendFreertos()
    # apply vfs related
    config.env.appendDefineFlags( [ 'MCUSH_VFS=%d'% int(hal_config.use_vfs) ] )
    if hal_config.use_vfs:
        config.env.appendDefineFlags( [ 'MCUSH_ROMFS=%d'% int(hal_config.use_romfs) ] )
        config.env.appendDefineFlags( [ 'MCUSH_FCFS=%d'% int(hal_config.use_fcfs) ] )
        config.env.appendDefineFlags( [ 'MCUSH_SPIFFS=%d'% int(hal_config.use_spiffs) ] )
        config.env.appendDefineFlags( [ 'MCUSH_FATFS=%d'% int(hal_config.use_fatfs) ] )
        if hal_config.use_spiffs:
            config.env.appendSpiffs()
        if hal_config.use_fatfs:
            config.env.appendFatfs()
    return config


