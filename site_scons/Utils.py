# MCUSH Scons Build Scripts, designed by Peng Shulin 
from time import strftime
from os import getenv
from binascii import hexlify


_SWITCH_CONFIRM = ['1', 'Y', 'y', 'T', 't', 'yes', 'Yes', 'YES', 'true', 'True', 'TRUE']

def getBoolEnv( name ):
    return bool( getenv(name) in _SWITCH_CONFIRM )

def generateBuildSignatureFile( fname='.build_signature' ):
    f = open(fname,'w+')
    f.write('/* Generated by MCUSH Scons Scripts */\n')
    f.write('__attribute__((section(".signature"))) __attribute__((used))\n')
    f.write('const char build_signature[] = "%s";\n'% strftime("%Y%m%d-%H%M%S"))
    f.close()
 

def char2wchar(char):
    return char+'\x00'

def chars2wchars(chars):
    return ''.join(map(char2wchar, chars))

