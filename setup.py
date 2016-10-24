from distutils.core import setup
import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(name='pandocfilters',
      version='1.4.0',
      description='Utilities for writing pandoc filters in python',
      long_description=read('README.rst'),
      author='John MacFarlane',
      author_email='fiddlosopher@gmail.com',
      url='http://github.com/jgm/pandocfilters',
      py_modules=['pandocfilters'],
      keywords=['pandoc'],
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Environment :: Console',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: BSD License',
          'Operating System :: OS Independent',
          'Programming Language :: Python',
          'Topic :: Text Processing :: Filters'
      ],
      )
