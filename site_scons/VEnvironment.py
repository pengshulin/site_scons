# MCUSH Scons Build Scripts, designed by Peng Shulin 
from SCons.Builder import Builder
from SCons.Action import Action
from SCons.Environment import Environment
from SCons.Errors import StopError
from SCons.Script import GetOption

from Toolchain import *
from Utils import *
import Utils

from os import environ, getenv, getcwd, system
from os.path import basename, abspath, isfile, join, splitext, dirname
from fnmatch import fnmatchcase
from time import strftime
from sys import path as sys_path
import sys
from subprocess import check_output


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
    name = None

    _TOOLCHAIN = Gcc

    # default flags
    _DEF_ASFLAGS = []
    _DEF_CCFLAGS = ['-std=c99', '-Wall',
                    #'-fmax-errors=10',
                    '-Wno-error=attributes',
                    '-Wextra',
                        #'-Wunused-but-set-variable', 
                        #'-Wno-unused-parameter',
                        #'-Wmaybe-uninitialized',
                        '-Wno-missing-field-initializers', 
                    '-Wformat=2',
                    '-Wformat-nonliteral',
                    #'-Wcast-align',
                    #'-Wsign-conversion',
                    #'-Wconversion',
                    '-Wfloat-conversion',
                    '-Wfloat-equal',
                    #'-Wno-sign-compare',
                    #'-Wcast-qual',
                    #'-Wmissing-prototypes',
                    #'-Wsign-conversion',
                    #'-Wmissing-field-initializers', 
                    #'-Wundef',
                    #'-Wno-error=stringop-truncation',
                    #'-pedantic', 
                    #'-Wdeclaration-after-statement',
                    '-fno-strict-aliasing',
                    '-ffunction-sections',
                    '-fdata-sections']
    _DEF_CPPPATH = []
    _DEF_LIBPATH = []
    _DEF_LIBS = ['m']
    _DEF_LINKFLAGS = ['-Wl,--gc-sections',
                      '-Wl,--print-memory-usage',
                      '-Wl,--cref']

    # additional flags
    _ASFLAGS = []
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

    _optimize_level = None


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

        self.Append( ASFLAGS=self._DEF_ASFLAGS )
        self.Append( CCFLAGS=self._DEF_CCFLAGS )
        self.Append( CPPPATH=self._DEF_CPPPATH )
        self.Append( LIBS=self._DEF_LIBS )
        self.Append( LIBPATH=self._DEF_LIBPATH )
        self.Append( LINKFLAGS=self._DEF_LINKFLAGS )

        self.Append( ASFLAGS=self._ASFLAGS )
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

    def appendAssemblerFlag( self, flag ):
        assert isinstance(flag, list) 
        self.Append( ASFLAGS=flag )
 
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
        if not GetOption('silent'):
            print( 'scons: root=' + self.root )
        
    def setName( self, name ):
        self.name = name

    def getName( self ):
        if self.name:
            return self.name
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
        if not name:
            name = self.getName()
        self.prepareLintEnv()

        # generate .build_signature file that contains "build date/time" 
        generateBuildSignatureFile()

        # compiler optimize flags and defination 
        self.appendCompilerFlag(['-g', '-Werror'])
        if self._optimize_level is None:
            self._optimize_level = 'O0' if self.DEBUG else 'O2'
        self.appendCompilerFlags(['-%s'% self._optimize_level])
        if self.DEBUG:
            self.appendDefineFlags(['DEBUG'])
        else:
            self.appendDefineFlags(['NDEBUG'])
       
        # set link file (.ld)
        if self.linkfile:
            linkfile_dir = dirname(self.linkfile)
            if linkfile_dir:
                # linkfile in different directory, append search path
                self.appendLinkFlag( ['-Wl,-L%s'% linkfile_dir] )
            self.appendLinkFlag( ['-Wl,-T%s'% self.linkfile] )
            
        #self.appendCompilerFlag( ['-DBUILD_DATE=%s'% self.BUILD_DATE] )
         
        # output map file
        self.appendLinkFlag( ['-Wl,--Map=%s.map'% name] )

        # build source files
        objs = []
        for sfile in self.source:
            obj = self.Object(sfile)
            objs.append( obj )
            if self.LINT:
                a, b = splitext(str(sfile))
                if b == '.c':
                    #self.AddPreAction(obj, self.splint_cmd)
                    self.AddPostAction(obj, self.splint_cmd)
         
        self.elffile = self.Program( name + '.elf', objs )
        self.binfile = self.Bin( name + '.bin', self.elffile )
        self.hexfile = self.Hex( name + '.hex', self.elffile )
        self.lstfile = self.Dump( name + '.lst', self.elffile )
        #self.mapfile = self.Map( name + '.map', self.elffile )
        self.Depends( self.binfile, self.elffile )
        self.Depends( self.hexfile, self.elffile )
        self.Depends( self.lstfile, self.elffile )
        #self.Depends( self.mapfile, self.elffile )
        self.Size( source=self.elffile )
        # append name target
        pathname = join(getcwd(), basename(name))
        self.AlwaysBuild( self.Alias('name', [], 'echo %s'% pathname) )

    def makeLib( self, name=None ):
        if not name:
            name = self.getName()
        self.prepareLintEnv()
        # sources files
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

    def makeMarkdownPdf( self, fname ):
        try:
            self.builder_md_pdf
        except AttributeError:
            self.builder_md_pdf = Builder(
                    action='markdown2pdf $SOURCES $TARGET',
                    suffix='.pdf', src_suffix='.md' )
            self.Append(BUILDERS = {'MarkdownPdf': self.builder_md_pdf})
        base = splitext(fname)[0]
        self.mdpdffile = self.MarkdownPdf(
                    target='%s.pdf'% base, source='%s.md'% base )

    def makeMarkdownHtml( self, fname ):
        try:
            self.builder_md_html
        except AttributeError:
            self.builder_md_html = Builder(
                    action='markdown $SOURCES >> $TARGET',
                    suffix='.pdf', src_suffix='.html' )
            self.Append(BUILDERS = {'MarkdownHtml': self.builder_md_html})
        base = splitext(fname)[0]
        self.mdhtmlfile = self.MarkdownHtml(
                    target='%s.html'% base, source='%s.md'% base )
        self.AddPostAction( self.mdhtmlfile, Action(
            'mv %s.html .html && \
             echo "<meta charset=utf8>" > .charset && \
             cat .charset .html > %s.html && \
             rm -f .charset .html'% (base, base)) )

    def makeMarkdownLandSlidePdf( self, fname ):
        try:
            self.builder_md_landslide_pdf
        except AttributeError:
            self.builder_md_landslide_pdf = Builder(
                    action='landslide $SOURCES -d $TARGET',
                    suffix='.pdf', src_suffix='.md' )
            self.Append(BUILDERS = {'MarkdownLandSlidePdf': self.builder_md_landslide_pdf})
        base = splitext(fname)[0]
        self.MarkdownLandSlidePdf( target='%s.pdf'% base, source='%s.md'% base )

    def makeMarkdownLandSlideHtml( self, fname ):
        try:
            self.builder_md_landslide_html
        except AttributeError:
            self.builder_md_landslide_html = Builder(
                    action='landslide $SOURCES -d $TARGET',
                    suffix='.html', src_suffix='.md' )
            self.Append(BUILDERS = {'MarkdownLandSlideHtml': self.builder_md_landslide_html})
        base = splitext(fname)[0]
        self.MarkdownLandSlideHtml( target='%s.html'% base, source='%s.md'% base )
    def setOptimizeLevel( self, level ):
        assert level in ['O0','O1','O2','O3','Os']
        self._optimize_level = level

    def appendDefineFlags( self, define_flags=None ):
        if define_flags is None:
            return
        transferd_flags = []
        for d in define_flags:
            quoting_mode = False
            hex_mode = False
            t = []
            d_len = len(d)
            for i, c in enumerate(d):
                if c == '\\':
                    t.append('\\\\')
                elif c in '\'\"':
                    if (not quoting_mode) or (i==(d_len-1)):
                        t.append('\\')
                        t.append(c)
                        quoting_mode = True
                    else:
                        t.append('\\\\x%X'% ord(c))
                elif (not quoting_mode) and (not hex_mode) and (33 <= ord(c) <= 126):
                    # all other printable chars except space
                    t.append(c)
                else:
                    t.append('\\\\x%X'% ord(c))
                    hex_mode = True
            t = ''.join(t)
            #print( "TRANSFER: " + d + ' --> ' + t + ' (' +  hexlify(t) + ')' )
            transferd_flags.append( t )
        #print( transferd_flags )
        self.appendCompilerFlag(['-D'+d for d in transferd_flags])



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

    # name aliases for mistype
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
   
    def appendFreeRTOS( self, heap=3 ):
        self.appendPath( [
            '/libFreeRTOS',
            '/libFreeRTOS/include',
            '/libFreeRTOS/portable/GCC/%s'% self.freertos_port,
            ] )
        self.appendGlobSource( [
            '/libFreeRTOS/*.c',
            '/libFreeRTOS/portable/GCC/%s/port.c'% self.freertos_port,
            ] )
        if isinstance(heap, int):
            self.appendGlobSource( [
                '/libFreeRTOS/portable/MemMang/heap_%d.c'% heap,
                ] )
    
    def appendRTX( self ):
        self.appendPath( [
            '/libRTX',
            ] )
        self.appendGlobSource( [
            '/libRTX/*.c',
            '/libRTX/GCC/%s.s'% self.rtx_irq_port,
            ] )

    def appendRTThread( self ):
        self.appendPath( [
            '/libRTThread/include',
            ] )
        self.appendGlobSource( [
            '/libRTThread/src/*.c',
            '/libRTThread/libcpu/arm/%s/*.c'% self._MCPU,
            '/libRTThread/libcpu/arm/%s/context_gcc.S'% self._MCPU,
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
    append_rtos = 'FreeRTOS'
    use_vfs = True
    use_romfs = True
    use_fcfs = None
    use_spiffs = None
    use_fatfs = None
    use_eth = None

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
    if not GetOption('silent'):
        if hal_config.__dict__:
            print( 'scons: hal_config(%s)'% (', '.join(['%s=%s'% (str(k),str(v)) for k,v in hal_config.__dict__.items()])) )
        else:
            print( 'scons: hal_config()' )
    # load from config.py
    import config as config
    config.env.haldir = haldir
    # NOTE: hal_config contents may be modified by 'import config'
    # auto load .c/.h sources
    if hal_config.append_hal:
        config.env.appendHal( haldir, hal_config.paths, hal_config.sources )
    if hal_config.append_mcush:
        config.env.appendMcush()
    if hal_config.append_rtos:
        hal_config.append_rtos = hal_config.append_rtos.strip().upper()
        if hal_config.append_rtos == 'FREERTOS':
            config.env.appendDefineFlags(['MCUSH_OS=OS_FREERTOS'])
            if hal_config.freertos_heap is None:
                config.env.appendFreeRTOS()
            else:
                config.env.appendFreeRTOS(heap=hal_config.freertos_heap)
        elif hal_config.append_rtos == 'RTX':
            config.env.appendDefineFlags(['MCUSH_OS=OS_RTX'])
            config.env.appendRTX()
        elif hal_config.append_rtos == 'THREADX':
            config.env.appendDefineFlags(['MCUSH_OS=OS_THREADX'])
            # TODO: add source codes
        elif hal_config.append_rtos == 'RTTHREAD':
            config.env.appendDefineFlags(['MCUSH_OS=OS_RTTHREAD'])
            config.env.appendRTThread()
    # apply vfs related
    config.env.appendDefineFlags( [ 'MCUSH_VFS=%d'% int(bool(hal_config.use_vfs)) ] )
    if hal_config.use_vfs:
        config.env.appendDefineFlags( [ 'MCUSH_ROMFS=%d'% int(bool(hal_config.use_romfs)) ] )
        config.env.appendDefineFlags( [ 'MCUSH_FCFS=%d'% int(bool(hal_config.use_fcfs)) ] )
        config.env.appendDefineFlags( [ 'MCUSH_SPIFFS=%d'% int(bool(hal_config.use_spiffs)) ] )
        config.env.appendDefineFlags( [ 'MCUSH_FATFS=%d'% int(bool(hal_config.use_fatfs)) ] )
        if hal_config.use_spiffs:
            config.env.appendSpiffs()
        if hal_config.use_fatfs:
            config.env.appendFatfs()
    return config


