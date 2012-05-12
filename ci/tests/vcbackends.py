from django.test import TestCase

from ci.models import Project, Commit, Build
from ci.plugins.base import Builder
from ci.tests.utils import VCS, default_branch

from vcs.exceptions import BranchDoesNotExistError

class PrivateProjectTests(TestCase):
    def setUp(self):
         # Project with two branches '$default_branch' and 'dev'.
        # Both branches get tested; docs are generated for '$default_branch' only.
        self.project = Project.objects.create(
            name='My super cool Project',
            slug='my-super-cool-project',
            vcs_type=VCS,
            private_key='somedata',
        )
        self.build_config = self.project.configurations.create(name='docs', branches=[default_branch])
    
    def test_private_repository_build(self):
        Repository = self.project.get_vcs_backend()
        assert getattr(Repository, 'supports_private_repositories', False)
        d1 = self.project.commits.create(branch='dev', vcs_id='dev1', was_successful=True)
        build = d1.builds.create(configuration=self.build_config)
        builder = Builder(build)
        try:
            builder.setup_build()
        except BranchDoesNotExistError:
            pass
        #TODO assert something
