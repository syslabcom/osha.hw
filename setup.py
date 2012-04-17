from setuptools import setup, find_packages
import os

version = '0.5dev'

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()
    

long_description = (
    read('README.txt')
    + '\n' +
    'Change history\n'
    '**************\n'
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    'Detailed Documentation\n'
    '**********************\n'
    + '\n' +
    'Contributors\n'
    '************\n'
    + '\n' +
    read('CONTRIBUTORS.txt')
    + '\n'
    )

setup(name='osha.hw',
      version=version,
      description="Healthy Workplaces for EU-OSHA",
      long_description=long_description,
      # Get more strings from
      # http://pypi.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Framework :: Zope2",
        "Framework :: Zope3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "License :: OSI Approved :: European Union Public Licence 1.1 (EUPL 1.1)",
        ],
      keywords='',
      author='Syslab.com GmbH',
      author_email='info@syslab.com',
      url='https://code.gocept.com/svn/osha/osha.hw/',
      license='gpl',
      packages=find_packages('src'),
      package_dir = {'': 'src'},
      namespace_packages=['osha', 'osha.hw'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'SQLAlchemy'
      ],
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """,
      )
