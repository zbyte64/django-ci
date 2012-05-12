from ci.plugins.toxplugin import ToxBuilder
from .plugins import BaseBuilderTests

sample_tox = '''
[tox]
envlist = 
    py27

[testenv]
commands = echo -n 1; echo -n 2
'''

sample_setup = '''
from distutils.core import setup; setup()
'''

class ToxBuilderTests(BaseBuilderTests):
    builder = ToxBuilder
    commits = [{'added': {'tox.ini': sample_tox, 
                          'setup.py':sample_setup,}}]
    
    def test_successful_build(self):
        super(ToxBuilderTests, self).test_successful_build()
        self.assertEqual(self.build.stderr.read(), '')
        self.assertTrue('[TOX] congratulations :)' in self.build.stdout.read())
    
    def break_build(self):
        self.commit({'message': "Broke the build", 'removed': ['setup.py']})
