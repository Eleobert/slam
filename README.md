[![License: Unlicense](https://img.shields.io/badge/license-Unlicense-blue.svg)](http://unlicense.org/)
## Slam

Slam is a cross-platform OpenGL function loader generator. Unlike most others OpenGL function generators the code generated by Slam is in modern C++ instead of C. All symbols are declared into a namespace and instead of relying in macros the library uses constexpr's. So using Slam you will not have any symbols messing the scope of your code.

#### Why another OpenGL function loader?

Because most of loaders around are written in C. So, those libraries does not limit their scope. A few others are written in C++ but they come with a lot of their own stuff that I (we) actually don't need.
One of the goals of Slam design is to be easy to integrate into other projects. You can specify to the loader your own C++ namespaces (even the new C++17 nested ones!).

For example:

```bash
slam-generator.py 4.4 --namespace my::engine
```
Every symbols (functions declarations and GLenum values) will be declared inside the namespace my::engine. So, in code you do:

```c++
my::engine::glClearCode(1.0f, 1.0f, 1.0f)
```
When generating code in compatibility profile you can tell slang-generator to mark deprecated functions and GLenum's values as `[[deprecated]]` (a C++14 feature), so you get a compiler warning when using them.

#### How to use Slam?
Slam is very easy to use, all you need to do is to add the .cpp and .h files to your project, or you can alternatively before build it as a library and link it. The files  in the directory named slam of this repository are ready to use, but you are also encouraged to generate it by your own using the slam-generator.py script. The reason is that, so, you can personalize the output files to feet your needs.


#### Using the script to generate the library
To generate you can use the following command:
```bash
slam-generator.py 4.6
```
This command generates the library to load functions for gl version 4.6 (gles and extensions still not supported). Note that some arguments are omitted. Bellow you see the table with all options


| Options        |Use |
|----------------|--------------|
|version         | any gl version, (non optional)               |
|--source        | name for the generated source files (without file extension), by default is "slang" |
|--source-dir | name for the generated source files directory, by default is "slang" |
|--profile       | compat or core, by default is core |
|-d              | when this flag is set the generator marks deprecated functions and enum values as deprecated (note that has no effect when generating in core profile)
|--namespace     | namespace to put the declarations, default is "gl" |
|--register| the path to the register file, default is "gl.xml"|

#### Minimal example

```c++
try
{
    //load the functions
    //throws an exception if OpenGL library could not be loaded
    gl::init();
}
catch(const std::runtime_error& e)
{
    std::cerr << e.what() << '\n';
    return -1;
}

std::cout << gl::glGetString(gl::GL_VERSION) << '\n';

gl::deinit(); //actually, we don't need to deinitialize
```
#### License
This software is dedicated to the public domain.