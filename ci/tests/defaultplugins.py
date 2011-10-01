from ci.plugins.defaultplugin import ShellBuilder
from .plugins import CommandBasedBuilderTests

class ShellBuilderTests(CommandBasedBuilderTests):
    builder = ShellBuilder

    def execute_build(self):
        self.config.parameters = self.repo.get_changeset().get_file_content('build.sh')
        self.config.save()
        self.builder.execute_build()
