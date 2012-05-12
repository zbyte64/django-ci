#!/usr/bin/env python

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

VERSION = '0.0.1'
LONG_DESC = """\
"""

setup(name='django-ci',
      version=VERSION,
      description="",
      long_description=LONG_DESC,
      classifiers=[
          'Programming Language :: Python',
          'Operating System :: OS Independent',
          'Natural Language :: English',
          'Development Status :: 3 - Alpha',
          'Intended Audience :: Developers',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
      ],
      keywords='django ci testing',
      #maintainer = 'Jason Kraus',
      #maintainer_email = ',
      url='https://github.com/jonashaag/django-ci',
      #license='New BSD License',
      packages=find_packages(exclude=['test_environment', 'tests']),
      test_suite='tests.setuptest.SetupTestSuite',
      tests_require=(
        'pep8',
        'coverage',
        'django',
      ),
      include_package_data = True,
  )
