import os
import sys

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.txt')).read()
CHANGES = open(os.path.join(here, 'CHANGES.txt')).read()

requires = [
    'pyramid',
    'SQLAlchemy',
    'transaction',
    'pyramid_tm',
    'pyramid_debugtoolbar',
    'zope.sqlalchemy',
    'waitress',
#    'pyramid>=1.1',
#    'SQLAlchemy>=0.7.1',
#    'transaction>=1.1.1',
#    'repoze.tm2>=1.0b1', # default_commit_veto
#    'zope.sqlalchemy',
#    'WebError>=0.10.3',
    ]

if sys.version_info[:3] < (2,5,0):
    requires.append('pysqlite')

setup(name='MotionMan',
      version='0.1',
      description='MotionMan',
      long_description=README + '\n\n' +  CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pylons",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='motionman',
      install_requires = requires,
      entry_points = """\
      [paste.app_factory]
      main = motionman:main

      [paste.app_install]
      main = motionman.lib.utils:PyramidInstaller
      """,
      paster_plugins=['pyramid'],
      )

