import os
import shutil
import tempfile
import traceback
from subprocess import Popen, PIPE

from ci.utils import BuildFailed

__all__ = ['Plugin', 'BuildHook', 'Builder', 'CommandBasedBuilder']

class Plugin(object):
    def get_builders(self):
        return {}

    def get_build_hooks(self):
        return {}

class BuildHook(object):
    def __init__(self, request):
        self.request = request

    def get_changed_branches(self):
        raise NotImplementedError

class Builder(object):
    def __init__(self, build):
        self.build = build

    def execute_build(self):
        try:
            self.setup_build()
            self.run()
            self.build.was_successful = True
        except BuildFailed:
            self.build.was_successful = False
        except:
            self.build.was_successful = False
            # XXX #16964
            if not self.build.stderr:
                self.build.stderr.save_named('', save=False)
            self.build.stderr.file.close()
            self.build.stderr.open('a')
            self.build.stderr.write(self.format_exception())
            self.build.stderr.close()
            self.build.stderr.open()
            raise
        finally:
            self.teardown_build()

    def setup_build(self):
        self.repo_path = tempfile.mkdtemp()
        os.rmdir(self.repo_path)
        self.repo = self.build.configuration.project.get_vcs_repository(repo_path=self.repo_path, update_after_clone=True, create=True)
        self.repo.workdir.checkout_branch(self.build.commit.branch)
        commit = self.build.commit
        if commit.vcs_id is None:
            changeset = self.repo.workdir.get_changeset()
            commit.vcs_id = changeset.raw_id
            commit.short_message = changeset.message.splitlines()[0]
            commit.save()
        assert os.path.exists(self.repo_path)

    def teardown_build(self):
        shutil.rmtree(self.repo_path, ignore_errors=True)

    def format_exception(self):
        return '\n\n' + '\n\n'.join([
            '=' * 79,
            "Exception in django-ci/builder",
            traceback.format_exc()
        ])

    def run(self):
        raise NotImplementedError


class CommandBasedBuilder(Builder):
    def run(self):
        cmd = self.get_cmd()
        # XXX directly pipe into files
        proc = Popen(cmd, cwd=self.repo_path, stdout=PIPE, stderr=PIPE)
        stdout, stderr = proc.communicate()
        self.build.stderr.save_named(stderr, save=False)
        self.build.stdout.save_named(stdout, save=False)
        if proc.returncode:
            raise BuildFailed("Command %s returned with code %d" % (cmd, proc.returncode))

    def get_cmd(self):
        return self.cmd
