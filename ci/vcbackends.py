#patches up vcs backends to handle private keys
import os

from vcs.backends.git import GitRepository
from vcs.conf.settings import BACKENDS

from subprocess import Popen, PIPE
from vcs.exceptions import RepositoryError

import tempfile

class PrivateGitRepository(GitRepository):
    private_key_path = None
    
    def set_private_key(self, payload):
        handle, path = tempfile.mkstemp()
        handle = open(path, 'w')
        handle.write(payload)
        handle.close()
        self.private_key_path = path
    
    def __delete__(self):
        if self.private_key_path:
            if os.path.exists(self.private_key_path):
                try:
                    os.unlink(self.private_key_path)
                except:
                    pass
    
    def run_git_command(self, cmd):
        """
        Runs given ``cmd`` as git command and returns tuple
        (returncode, stdout, stderr).

        .. note::
           This method exists only until log/blame functionality is implemented
           at Dulwich (see https://bugs.launchpad.net/bugs/645142). Parsing
           os command's output is road to hell...

        :param cmd: git command to be executed
        """
        #cmd = '(cd %s && git %s)' % (self.path, cmd)
        if isinstance(cmd, basestring):
            cmd = 'git %s' % cmd
        else:
            cmd = ' '.join(['git'] + cmd)
        try:
            opts = dict(
                shell=isinstance(cmd, basestring),
                stdout=PIPE,
                stderr=PIPE)
            if os.path.isdir(self.path):
                opts['cwd'] = self.path
            if self.private_key_path:
                cmd = ['ssh-agent', 'bash', '-c', 'ssh-add %s && %s' % (self.private_key_path, cmd)]
            p = Popen(cmd, **opts)
        except OSError, err:
            raise RepositoryError("Couldn't run git command (%s).\n"
                "Original error was:%s" % (cmd, err))
        so, se = p.communicate()
        if not se.startswith("fatal: bad default revision 'HEAD'") and \
            p.returncode != 0:
            raise RepositoryError("Couldn't run git command (%s).\n"
                "stderr:\n%s" % (cmd, se))
        return so, se

BACKENDS['git'] = 'ci.vcbackends.PrivateGitRepository'
