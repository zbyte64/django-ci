import os
from ci.plugins import Plugin, CommandBasedBuilder
from ci.utils import BuildFailed

class TravisBuilder(CommandBasedBuilder):
    command_keywords = ['before_install',
                        'install',
                        'after_install',
                        'before_script', 
                        'script', 
                        'after_script']
    def get_cmd(self):
        import yaml
        travis_config_path = os.path.join(self.repo_path, '.travis.yml')
        if not os.path.isfile(travis_config_path):
            raise BuildFailed('.travis.yml not found')
        travis_config = yaml.load(open(travis_config_path, 'r').read())
        language = travis_config.get('language', 'python')
        #TODO setup virtualenv for the specified version of python
        
        commands = list()
        for key in self.command_keywords:
            if key in travis_config:
                value = travis_config[key]
                if isinstance(value, basestring):
                    commands.append(value)
                else:
                    commands.extend(value)
            elif key == 'install':
                if 'requirements' in travis_config:
                    pass
        envs = travis_config.get('env', None)
        #TODO support builds that can update configurations
        if envs:
            if isinstance(envs, basestring):
                envs = [envs]
            test_commands = commands
            commands = list()
            for env in envs:
                cmds = [env] + test_commands
                commands.extend(cmds)
                #TODO be able to set up environs
        return [os.environ.get('SHELL', '/bin/sh'), '-c', ' && '.join(commands)] #TODO builders should be able to define tasks

class DefaultPlugin(Plugin):
    def get_builders(self):
        return {'travis': TravisBuilder}
