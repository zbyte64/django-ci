from ci.plugins.travisplugin import TravisBuilder
from .plugins import BaseBuilderTests

sample_travis = '''
language: python
script:
  - echo -n 1; echo -n 2
'''

sample_setup = '''
from distutils.core import setup; setup()
'''

class TravisBuilderTests(BaseBuilderTests):
    builder = TravisBuilder
    commits = [{'added': {'.travis.yml': sample_travis, 
                          'setup.py':sample_setup,}}]
    
    def break_build(self):
        self.commit({'message': "Broke the build", 'removed': ['.travis.yml']})
