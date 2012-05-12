import os
from ci.plugins import Plugin, CommandBasedBuilder

class ToxBuilder(CommandBasedBuilder):
    def get_cmd(self):
        return [os.environ.get('TOX', 'tox'),]

class DefaultPlugin(Plugin):
    def get_builders(self):
        return {'shell': ToxBuilder}
