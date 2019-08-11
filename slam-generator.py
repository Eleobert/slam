#!/usr/bin/python3

import argparse
import xml.etree.ElementTree as ElTree
import os
import tempfile
import sys

tab = '    '

glenums = []
glfunctions = []

header = tempfile.NamedTemporaryFile(mode='w', delete = False)
source = tempfile.NamedTemporaryFile(mode='w', delete = False)

source_path = str()
header_path = str()


parser = argparse.ArgumentParser(description='This script generates a C++ OpenGL function loader library.')

parser.add_argument('api', action = 'store', nargs='+', help = "API and version eg. 'gl 4.0'")

parser.add_argument('--source-dir', action = 'store', default = 'slam', type = str,
                        help = "name for the generated source files directory, by default is 'slam'")

parser.add_argument('--source', action = 'store', default = 'slam', type = str,
                        help = "name for the generated source files directory, by default is 'slam'")

parser.add_argument('--profile', action = 'store', choices = ['compat', 'core'], default = 'core',
                        help = "specify the OpenGL profile mode, if core, deprecated features will not to be \
                                generated")

parser.add_argument("--namespace", action = 'store', type = str, default = 'gl',
                        help = 'name of the global C++ namespace, \
                        the default is \'gl\'')

parser.add_argument("-d", action = 'store_true', default = False,
                        help = "marks deprecated features as deprecated")

parser.add_argument("--register", action = 'store', metavar='NAME', type = str,
                        help = "name of the xml register file, by default is 'gl.xml'")


args = parser.parse_args()

khrplatform_code = """#ifndef __khrplatform_h_
#define __khrplatform_h_

/*
** Copyright (c) 2008-2018 The Khronos Group Inc.
**
** Permission is hereby granted, free of charge, to any person obtaining a
** copy of this software and/or associated documentation files (the
** "Materials"), to deal in the Materials without restriction, including
** without limitation the rights to use, copy, modify, merge, publish,
** distribute, sublicense, and/or sell copies of the Materials, and to
** permit persons to whom the Materials are furnished to do so, subject to
** the following conditions:
**
** The above copyright notice and this permission notice shall be included
** in all copies or substantial portions of the Materials.
**
** THE MATERIALS ARE PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
** EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
** MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
** IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
** CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
** TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
** MATERIALS OR THE USE OR OTHER DEALINGS IN THE MATERIALS.
*/

/* Khronos platform-specific types and definitions.
 *
 * The master copy of khrplatform.h is maintained in the Khronos EGL
 * Registry repository at https://github.com/KhronosGroup/EGL-Registry
 * The last semantic modification to khrplatform.h was at commit ID:
 *      67a3e0864c2d75ea5287b9f3d2eb74a745936692
 *
 * Adopters may modify this file to suit their platform. Adopters are
 * encouraged to submit platform specific modifications to the Khronos
 * group so that they can be included in future versions of this file.
 * Please submit changes by filing pull requests or issues on
 * the EGL Registry repository linked above.
 *
 *
 * See the Implementer's Guidelines for information about where this file
 * should be located on your system and for more details of its use:
 *    http://www.khronos.org/registry/implementers_guide.pdf
 *
 * This file should be included as
 *        #include <KHR/khrplatform.h>
 * by Khronos client API header files that use its types and defines.
 *
 * The types in khrplatform.h should only be used to define API-specific types.
 *
 * Types defined in khrplatform.h:
 *    khronos_int8_t              signed   8  bit
 *    khronos_uint8_t             unsigned 8  bit
 *    khronos_int16_t             signed   16 bit
 *    khronos_uint16_t            unsigned 16 bit
 *    khronos_int32_t             signed   32 bit
 *    khronos_uint32_t            unsigned 32 bit
 *    khronos_int64_t             signed   64 bit
 *    khronos_uint64_t            unsigned 64 bit
 *    khronos_intptr_t            signed   same number of bits as a pointer
 *    khronos_uintptr_t           unsigned same number of bits as a pointer
 *    khronos_ssize_t             signed   size
 *    khronos_usize_t             unsigned size
 *    khronos_float_t             signed   32 bit floating point
 *    khronos_time_ns_t           unsigned 64 bit time in nanoseconds
 *    khronos_utime_nanoseconds_t unsigned time interval or absolute time in
 *                                         nanoseconds
 *    khronos_stime_nanoseconds_t signed time interval in nanoseconds
 *    khronos_boolean_enum_t      enumerated boolean type. This should
 *      only be used as a base type when a client API's boolean type is
 *      an enum. Client APIs which use an integer or other type for
 *      booleans cannot use this as the base type for their boolean.
 *
 * Tokens defined in khrplatform.h:
 *
 *    KHRONOS_FALSE, KHRONOS_TRUE Enumerated boolean false/true values.
 *
 *    KHRONOS_SUPPORT_INT64 is 1 if 64 bit integers are supported; otherwise 0.
 *    KHRONOS_SUPPORT_FLOAT is 1 if floats are supported; otherwise 0.
 *
 * Calling convention macros defined in this file:
 *    KHRONOS_APICALL
 *    KHRONOS_APIENTRY
 *    KHRONOS_APIATTRIBUTES
 *
 * These may be used in function prototypes as:
 *
 *      KHRONOS_APICALL void KHRONOS_APIENTRY funcname(
 *                                  int arg1,
 *                                  int arg2) KHRONOS_APIATTRIBUTES;
 */

/*-------------------------------------------------------------------------
 * Definition of KHRONOS_APICALL
 *-------------------------------------------------------------------------
 * This precedes the return type of the function in the function prototype.
 */
#if defined(_WIN32) && !defined(__SCITECH_SNAP__)
#   define KHRONOS_APICALL __declspec(dllimport)
#elif defined (__SYMBIAN32__)
#   define KHRONOS_APICALL IMPORT_C
#elif defined(__ANDROID__)
#   define KHRONOS_APICALL __attribute__((visibility("default")))
#else
#   define KHRONOS_APICALL
#endif

/*-------------------------------------------------------------------------
 * Definition of KHRONOS_APIENTRY
 *-------------------------------------------------------------------------
 * This follows the return type of the function  and precedes the function
 * name in the function prototype.
 */
#if defined(_WIN32) && !defined(_WIN32_WCE) && !defined(__SCITECH_SNAP__)
    /* Win32 but not WinCE */
#   define KHRONOS_APIENTRY __stdcall
#else
#   define KHRONOS_APIENTRY
#endif

/*-------------------------------------------------------------------------
 * Definition of KHRONOS_APIATTRIBUTES
 *-------------------------------------------------------------------------
 * This follows the closing parenthesis of the function prototype arguments.
 */
#if defined (__ARMCC_2__)
#define KHRONOS_APIATTRIBUTES __softfp
#else
#define KHRONOS_APIATTRIBUTES
#endif

/*-------------------------------------------------------------------------
 * basic type definitions
 *-----------------------------------------------------------------------*/
#if (defined(__STDC_VERSION__) && __STDC_VERSION__ >= 199901L) || defined(__GNUC__) || defined(__SCO__) || defined(__USLC__)


/*
 * Using <stdint.h>
 */
#include <stdint.h>
typedef int32_t                 khronos_int32_t;
typedef uint32_t                khronos_uint32_t;
typedef int64_t                 khronos_int64_t;
typedef uint64_t                khronos_uint64_t;
#define KHRONOS_SUPPORT_INT64   1
#define KHRONOS_SUPPORT_FLOAT   1

#elif defined(__VMS ) || defined(__sgi)

/*
 * Using <inttypes.h>
 */
#include <inttypes.h>
typedef int32_t                 khronos_int32_t;
typedef uint32_t                khronos_uint32_t;
typedef int64_t                 khronos_int64_t;
typedef uint64_t                khronos_uint64_t;
#define KHRONOS_SUPPORT_INT64   1
#define KHRONOS_SUPPORT_FLOAT   1

#elif defined(_WIN32) && !defined(__SCITECH_SNAP__)

/*
 * Win32
 */
typedef __int32                 khronos_int32_t;
typedef unsigned __int32        khronos_uint32_t;
typedef __int64                 khronos_int64_t;
typedef unsigned __int64        khronos_uint64_t;
#define KHRONOS_SUPPORT_INT64   1
#define KHRONOS_SUPPORT_FLOAT   1

#elif defined(__sun__) || defined(__digital__)

/*
 * Sun or Digital
 */
typedef int                     khronos_int32_t;
typedef unsigned int            khronos_uint32_t;
#if defined(__arch64__) || defined(_LP64)
typedef long int                khronos_int64_t;
typedef unsigned long int       khronos_uint64_t;
#else
typedef long long int           khronos_int64_t;
typedef unsigned long long int  khronos_uint64_t;
#endif /* __arch64__ */
#define KHRONOS_SUPPORT_INT64   1
#define KHRONOS_SUPPORT_FLOAT   1

#elif 0

/*
 * Hypothetical platform with no float or int64 support
 */
typedef int                     khronos_int32_t;
typedef unsigned int            khronos_uint32_t;
#define KHRONOS_SUPPORT_INT64   0
#define KHRONOS_SUPPORT_FLOAT   0

#else

/*
 * Generic fallback
 */
#include <stdint.h>
typedef int32_t                 khronos_int32_t;
typedef uint32_t                khronos_uint32_t;
typedef int64_t                 khronos_int64_t;
typedef uint64_t                khronos_uint64_t;
#define KHRONOS_SUPPORT_INT64   1
#define KHRONOS_SUPPORT_FLOAT   1

#endif


/*
 * Types that are (so far) the same on all platforms
 */
typedef signed   char          khronos_int8_t;
typedef unsigned char          khronos_uint8_t;
typedef signed   short int     khronos_int16_t;
typedef unsigned short int     khronos_uint16_t;

/*
 * Types that differ between LLP64 and LP64 architectures - in LLP64,
 * pointers are 64 bits, but 'long' is still 32 bits. Win64 appears
 * to be the only LLP64 architecture in current use.
 */
#ifdef _WIN64
typedef signed   long long int khronos_intptr_t;
typedef unsigned long long int khronos_uintptr_t;
typedef signed   long long int khronos_ssize_t;
typedef unsigned long long int khronos_usize_t;
#else
typedef signed   long  int     khronos_intptr_t;
typedef unsigned long  int     khronos_uintptr_t;
typedef signed   long  int     khronos_ssize_t;
typedef unsigned long  int     khronos_usize_t;
#endif

#if KHRONOS_SUPPORT_FLOAT
/*
 * Float type
 */
typedef          float         khronos_float_t;
#endif

#if KHRONOS_SUPPORT_INT64
/* Time types
 *
 * These types can be used to represent a time interval in nanoseconds or
 * an absolute Unadjusted System Time.  Unadjusted System Time is the number
 * of nanoseconds since some arbitrary system event (e.g. since the last
 * time the system booted).  The Unadjusted System Time is an unsigned
 * 64 bit value that wraps back to 0 every 584 years.  Time intervals
 * may be either signed or unsigned.
 */
typedef khronos_uint64_t       khronos_utime_nanoseconds_t;
typedef khronos_int64_t        khronos_stime_nanoseconds_t;
#endif

/*
 * Dummy value used to pad enum types to 32 bits.
 */
#ifndef KHRONOS_MAX_ENUM
#define KHRONOS_MAX_ENUM 0x7FFFFFFF
#endif

/*
 * Enumerated boolean type
 *
 * Values other than zero should be considered to be true.  Therefore
 * comparisons should not be made against KHRONOS_TRUE.
 */
typedef enum {
    KHRONOS_FALSE = 0,
    KHRONOS_TRUE  = 1,
    KHRONOS_BOOLEAN_ENUM_FORCE_SIZE = KHRONOS_MAX_ENUM
} khronos_boolean_enum_t;

#endif /* __khrplatform_h_ */"""


class Enum:
    valtype = 'GLenum'
    name = str()
    value = str()
    deprecated = False

    _format = '{:60}'

    def __init__(self, valtype, name, value):
        self.name  = name
        self.value = value

        if valtype != None:
            if valtype == 'u':              #uint
                self.valtype = 'GLenum'
            
            if valtype == 'ull':            #unsigned long long
                self.valtype = 'GLuint64'

    def declaration(self):

        aux = str()
        if self.deprecated and args.d:
            aux += '[[deprecated]] '
        aux += "constexpr " + self.valtype + ' ' + self.name
        s = tab + self._format.format(aux)
        s+= " = " + self.value + ';\n'
        return s


class Function:
    rettype = str()
    name = str()
    args = []         #list of tuples
    deprecated = False

    def __init__(self, rettype, name, args):
        self.rettype = rettype
        self.name = name
        self.args = args

    def _helper(self):
        s = self.rettype + ' (APIENTRY *' + self.name
        s+= ') ('
        for i in range(len(self.args)):
            s += self.args[i]['type'] + ' ' + self.args[i]['name']
            
            if i != (len(self.args) - 1): #if it's the last parameter
                s += ', '
        s+=')'
        return s

    def declaration(self):
        s = tab
        if args.d and self.deprecated:
            s += ' [[deprecated]]'
        s += ' extern '
            
        s += self._helper() + ';\n'
        return s
    
    def definition(self):
        s = tab  + self._helper() + ' = nullptr;\n'
        return s
    
    def load(self):
        s = 2 * tab + self.name
        s+= ' = (decltype(' + self.name + ')) load(\"' + self.name + '\");\n'
        return s


def write_function_pointers_declarations():
    for function in glfunctions:
        header.write(function.declaration())

def write_function_pointers_definitions():
    for function in glfunctions:
       source.write(function.definition())
        

def write_header_file():
    header.write("""#pragma once

#ifdef __gl_h_
    #error Do not include OpenGL  before this header
#endif
#define __gl_h_

#include <KHR/khrplatform.h>

#ifdef _WIN32
#define APIENTRY __stdcall
#else 
#define APIENTRY
#endif


namespace """)
    header.write(args.namespace)
    header.write('\n{\n\n')
    s = tab + 'void init();\n' + tab + 'void deinit();\n\n'
    header.write(s)
    write_types_declaration()
    header.write('\n\n')
    
    for enum in glenums:
        header.write(enum.declaration())

    header.write('\n\n')
    
    for function in glfunctions:
        header.write(function.declaration())
    header.write('\n}\n#undef APIENTRY')


def write_types_declaration():
    for type in root.find('types'):
        if type.get('name') == 'khrplatform':
            continue
        if type.text == None:
            continue

        if type.find('apientry') != None:
            s = tab + type.text + 'APIENTRY ' + type.find('apientry').tail
            s += type.find('name').text + type.find('name').tail

        else:
            s =  tab + type.text
            if type.find('name') != None:
                s += type.find('name').text + type.find('name').tail
        
        s+='\n'
        header.write(s)

def write_source_file():
    s = '#include <' + header_path + '>'
    source.write(s)
    source.write("""

#ifdef _WIN32
#ifndef WIN32_LEAN_AND_MEAN
#define WIN32_LEAN_AND_MEAN 
    #include <windows.h>
#endif
#else 
    #include <dlfcn.h>
#endif

#include <string>
#include <iostream>
#include <cassert>


#ifdef _WIN32
static HMODULE libGL;
   #ifndef APIENTRY 
      #define APIENTRY _stdcall
   #endif
#else 
static void* libGL = nullptr;
#endif

#ifndef _WIN32
      #define APIENTRY
#endif

#ifndef __APPLE__
    void* (APIENTRY *getProcAddress) (const char*) = nullptr;
#endif


#ifdef _MSC_VER
#pragma warning(disable: 4996)
#else
#pragma push
#pragma GCC diagnostic ignored "-Wdeprecated-declarations"
#endif
""")
    s = '\n\nnamespace ' + args.namespace + '\n{'
    source.write(s)

    slam_functions_str = """
    void openlibGL()
    {
    #ifdef _WIN32
        libGL = LoadLibraryW(L"opengl32.dll");
    #elif __APPLE__
        libGL = dlopen("/System/Library/Frameworks/OpenGL.framework/OpenGL", RTLD_NOW | RTLD_GLOBAL);
    #else
        libGL = dlopen("libGL.so", RTLD_NOW | RTLD_GLOBAL);
    #endif
        if(libGL == nullptr)
        {
            throw std::runtime_error("Opengl library could not be loaded");
        }
    #ifndef __APPLE__
    #ifdef _WIN32
        getProcAddress = (decltype(getProcAddress))GetProcAddress(libGL, "wglGetProcAddress");
    #else
        getProcAddress = (decltype(getProcAddress)) dlsym(libGL, "glXGetProcAddressARB");
    #endif
        if(getProcAddress == nullptr)
        {
            throw std::runtime_error("Could not load OpenGL function loader.");
        }
    #endif
    }

    void deinit(void)
    {
        if(libGL != NULL) 
        { 
            #ifdef _WIN32
                FreeLibrary((HMODULE) libGL);
            #else
                dlclose(libGL);
            #endif
            libGL = nullptr;
        }
    }

    static void* load(const char *name) 
    {
        void* result = nullptr;
        assert(libGL != nullptr);

    #ifndef __APPLE__
        if(getProcAddress != nullptr)
        {
            result = (void*)getProcAddress(name);
        }
    #endif

        if(result == nullptr)
        {
            #ifdef _WIN32
                result = (void*)GetProcAddress(libGL, name);
            #else
                result = dlsym(libGL, name);
            #endif
        }
        return result;
    }"""

    source.write(slam_functions_str)
    source.write('\n\n')
    write_function_pointers_definitions()
    source.write('\n\n')
    write_function_open()
    source.write("""
}
#ifdef _MSC_VER
#pragma warning(push)
#else
#pragma pop
#endif""")


def write_function_open():
    s = tab + 'void init()' + '\n' + tab + '{\n' + (2*tab) + 'openlibGL();\n'
    source.write(s)
    for function in glfunctions:
        source.write(function.load())
    s = tab + '}'
    source.write(s)
    

def parse_enum():
    all_enums = {}
    
    #load all the enumeration elements and it's values
    for enums in root.findall("enums"):
        for enum in enums.findall("enum"):
            name = enum.get('name')
            all_enums[name] = Enum(enum.get('type'), name, enum.get('value'))
    
    #loop thougth gl versions
    for feature in tree.findall('feature'):
        #ignore all the higher versions
        if (float(feature.get('number')) > args.number) or feature.get('api') != 'gl':
            continue

        #set elements as deprecated
        for remove in feature.findall('remove'):
            if remove != None:
                for enum in remove:
                    all_enums[name].deprecated = True
    
                
        #now load it for real
        for require in feature.findall('require'):
            for element in require.findall('enum'):
                temp = all_enums[element.get('name')]
                if temp not in glenums:
                    glenums.append(temp)


def load_deprecated_functions_names(feature_node):
    deprecated = []
    for remove in feature_node.findall('remove'):
        if remove != None:
            for command in remove.findall('command'):
                deprecated.append(command.get('name'))
    return deprecated

def load_deprecated_enums_names(feature_node):
    deprecated = []
    for remove in feature_node.findall('remove'):
        if remove != None:
            for enum in remove.findall('enum'):
                deprecated.append(enum.get('name'))
    return deprecated


def load_function(command_node, deprecated_functions):
    proto = command_node.find('proto')
    function_name = proto.find('name').text
    rettype = str()
    if proto.text != None:
        rettype = proto.text
    if proto.find('ptype') != None:
        rettype += proto.find('ptype').text + proto.find('ptype').tail
    
    #find the parameters
    fargs = []
    for param in command_node.findall('param'):
        temp = {}
        temp['name'] = param.find('name').text
        temp['type'] = str()
        if param.text != None: #for const arguments
            temp['type'] = param.text
        aux = param.find('ptype')
        if aux != None:
            temp['type'] += aux.text + aux.tail

        fargs.append(temp)
    function = Function(rettype, function_name, fargs)
    if function_name in deprecated_functions:
        function.deprecated = True
    return function

def load_required_functions_names(feature):
    required = []
    for require in feature.findall('require'):
        for command in require.findall('command'):
            required.append(command.get('name'))
    return required

def load_required_enums_names(feature):
    required = []
    for require in feature.findall('require'):
        for enum in require.findall('enum'):
            required.append(enum.get('name'))
    return required

def parse_enums(api, version):
    enums_names_to_load = []
    deprecated = []
    for feature in tree.findall('feature'):
        if (float(feature.get('number')) > version) or feature.get('api') != api:
            continue

        current_deprecated = load_deprecated_enums_names(feature)
        current_required = load_required_enums_names(feature)
        
        if args.profile == 'core':
            for enum_name in current_deprecated:
                enums_names_to_load.remove(enum_name)
        
        for enum_name in current_required:
            enums_names_to_load.append(enum_name)
            if enum_name in deprecated: 
                #remove enum previously set as deprecated
                #a few enums need it
                deprecated.remove(enum_name)

        deprecated += current_deprecated
        
    for enums in root.findall('enums'):
        for enum in enums.findall("enum"):
            name = enum.get('name')
            if name in enums_names_to_load:
                e = Enum(enum.get('type'), enum.get('name'), enum.get('value'))
                if name in deprecated:
                    e.deprecated = True
                glenums.append(e)

def parse_functions(api, version):
    functions_names_to_load = []
    deprecated = []
    for feature in tree.findall('feature'):
        if (float(feature.get('number')) > version) or feature.get('api') != api:
            continue

        current_deprecated = load_deprecated_functions_names(feature)
        current_required = load_required_functions_names(feature)

        if args.profile == 'core':
            for function_name in current_deprecated:
                functions_names_to_load.remove(function_name)
        
        for function_name in current_required:
            functions_names_to_load.append(function_name)
            if function_name in deprecated: 
                #remove function previously set as deprecated
                #a few functions need it eg. glGetPointer
                deprecated.remove(function_name)

        deprecated += current_deprecated
        
    for command in root.find('commands').findall("command"):
        name = command.find('proto').find('name').text
        if name in functions_names_to_load:
            glfunctions.append(load_function(command, deprecated))


def done(code):
    header.close()
    source.close()
    exit(code)

def check_if_API_and_version_exists(root, api, version):
    for feature in root.findall('feature'):
        if feature.get('api') == api and float(feature.get('number')) == version:
            return
    print("Error: no API '", api, " ", version, "'", sep = '')


def check_api_command_argument(root, api_arg):
    if len(api_arg) != 2:
        print("Error: wrong api argument ",api_arg,", do '<api> <version>'", sep = '', file=sys.stderr)
        done(-1)

    try:
        float(api_arg[1])
    except ValueError:
        print("Error: invalid api version: '", api_arg[1], "'", sep ='')
        done(-1)

    check_if_API_and_version_exists(root, api_arg[0], float(api_arg[1]))
    return (api_arg[0], float(api_arg[1]))


if args.register:
    filename =  args.register
else:
    filename = os.path.dirname(os.path.realpath(__file__)) + "/gl.xml"

try:
    tree = ElTree.parse(filename)
except FileNotFoundError:
    print("Error: register file '", filename, "' not found.", sep = '', file=sys.stderr)
    done(-1)
except:
    print("Error: register file '", filename, "' could not be parsed.", sep = '', file=sys.stderr)
    done(-1)



if args.profile == 'core' and args.d == True:
    print("When compiling with '--profile core' flag 'd' (deprecate) has no effect", file=sys.stderr)

root = tree.getroot()

api_version = check_api_command_argument(root, args.api)

if not args.source_dir == '':
    if not os.path.exists(args.source_dir):
        os.makedirs(args.source_dir)
    if args.source_dir[-1] != '/':
        args.source_dir += '/' 

header_path = args.source_dir + args.source + '.h'
source_path = args.source_dir + args.source + '.cpp'

parse_enums(api_version[0], api_version[1])
parse_functions(api_version[0], api_version[1])

write_header_file() 
write_source_file()

temp_header_name = header.name
temp_source_name = source.name


header.close()
source.close()

os.replace(temp_header_name, header_path)
os.replace(temp_source_name, source_path)

if not os.path.exists(args.source_dir + 'KHR/'):
    os.makedirs(args.source_dir + 'KHR')
khrplatform = open(args.source_dir + 'KHR/khrplatform.h', 'w')

khrplatform.write(khrplatform_code)
