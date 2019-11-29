import sys
import tempfile
from collections import defaultdict
from distutils.ccompiler import CCompiler
from distutils.errors import CompileError
from pathlib import Path

import pybind11
from setuptools import (Extension,
                        find_packages,
                        setup)
from setuptools.command.build_ext import build_ext

import martinez


def has_flag(compiler: CCompiler, name: str) -> bool:
    """Detects whether a flag name is supported on the specified compiler."""
    with tempfile.NamedTemporaryFile('w',
                                     suffix='.cpp') as f:
        f.write('int main (int argc, char **argv) { return 0; }')
        try:
            compiler.compile([f.name],
                             extra_postargs=[name])
        except CompileError:
            return False
    return True


def cpp_flag(compiler: CCompiler) -> str:
    """
    Returns the -std=c++[11/14/17] compiler flag.
    The newer version is preferred when available.
    """
    flags = ['-std=c++17', '-std=c++14', '-std=c++11']
    for flag in flags:
        if has_flag(compiler, flag):
            return flag
    raise RuntimeError('Unsupported compiler: '
                       'at least C++11 support is needed!')


class BuildExt(build_ext):
    """A custom build extension for adding compiler-specific options."""
    c_opts = defaultdict(list,
                         {'msvc': ['/EHsc'],
                          'unix': []})
    l_opts = defaultdict(list,
                         {'msvc': [],
                          'unix': []})

    if sys.platform == 'darwin':
        darwin_opts = ['-stdlib=libc++', '-mmacosx-version-min=10.7']
        c_opts['unix'] += darwin_opts
        l_opts['unix'] += darwin_opts

    def build_extensions(self):
        compiler_type = self.compiler.compiler_type
        print('compiler type', compiler_type)
        opts = self.c_opts[compiler_type]
        link_opts = self.l_opts[compiler_type]
        if compiler_type == 'unix':
            opts.append('-DVERSION_INFO="{}"'
                        .format(self.distribution.get_version()))
            opts.append(cpp_flag(self.compiler))
            if has_flag(self.compiler, '-fvisibility=hidden'):
                opts.append('-fvisibility=hidden')
        elif compiler_type == 'msvc':
            opts.append('/DVERSION_INFO=\\"{}\\"'
                        .format(self.distribution.get_version()))
        for ext in self.extensions:
            ext.extra_compile_args = opts
            ext.extra_link_args = link_opts
        build_ext.build_extensions(self)


project_base_url = 'https://github.com/lycantropos/martinez/'

setup(name=martinez.__name__,
      packages=find_packages(exclude=('tests', 'tests.*')),
      version=martinez.__version__,
      description=martinez.__doc__,
      long_description=Path('README.md').read_text(encoding='utf-8'),
      long_description_content_type='text/markdown',
      author='Azat Ibrakov',
      author_email='azatibrakov@gmail.com',
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.5',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: Implementation :: CPython',
      ],
      license='MIT License',
      url=project_base_url,
      download_url=project_base_url + 'archive/master.zip',
      python_requires='>=3.5',
      install_requires=Path('requirements.txt').read_text(),
      cmdclass={'build_ext': BuildExt},
      ext_modules=[Extension('_' + martinez.__name__,
                             ['src/main.cpp'],
                             include_dirs=[pybind11.get_include(),
                                           pybind11.get_include(True)],
                             language='c++')],
      zip_safe=False)
