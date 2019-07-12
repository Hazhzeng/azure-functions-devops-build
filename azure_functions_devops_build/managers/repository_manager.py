# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ..base.base_information import BaseInformation
from ..clients.client_factory import ClientFactory
from ..utils.local_git_utils import (
    git_init,
    git_add_remote,
    git_remove_remote,
    git_stage_all,
    git_commit,
    git_push,
    does_git_exist,
    does_local_git_repository_exist,
    does_git_has_credential_manager,
    does_git_remote_exist,
    construct_git_remote_name,
    construct_git_remote_url)


class RepositoryManager(object):

    def __init__(self, organization_name="", project_name="", creds=None):
        self._information = BaseInformation(
            organization=organization_name,
            project=project_name,
            credential=creds)
        self._core = ClientFactory.get_core_client(self._information)
        self._git = ClientFactory.get_git_client(self._information)

    @staticmethod
    def check_git():
        return does_git_exist()

    @staticmethod
    def check_git_local_repository():
        return does_local_git_repository_exist()

    @staticmethod
    def check_git_credential_manager():
        return does_git_has_credential_manager()

    # Check if the git repository exists first. If it does, check if the git remote exists.
    def check_git_remote(self, repository_name, remote_prefix):
        if not does_local_git_repository_exist():
            return False

        remote_name = construct_git_remote_name(
            organization_name=self._information.get_organization(),
            project_name=self._information.get_project(),
            repository_name=repository_name,
            remote_prefix=remote_prefix)
        return does_git_remote_exist(remote_name)

    def remove_git_remote(self, repository_name, remote_prefix):
        remote_name = construct_git_remote_name(
            organization_name=self._information.get_organization(),
            project_name=self._information.get_project(),
            repository_name=repository_name,
            remote_prefix=remote_prefix)
        git_remove_remote(remote_name)

    def get_azure_devops_repository_branches(self, repository_name):
        return self._git.get_branches(repository_name)

    def get_azure_devops_repository(self, repository_name):
        return self._git.get_repository_by_name(repository_name)

    def create_repository(self, repository_name):
        project_obj = self._core.get_project_by_name()
        return self._git.create_repository(repository_name, project_obj)

    def list_repositories(self):
        return self._git.get_repositories()

    def get_local_git_remote_name(self, repository_name, remote_prefix):
        return construct_git_remote_name(
            organization_name=self._information.get_organization(),
            project_name=self._information.get_project(),
            repository_name=repository_name,
            remote_prefix=remote_prefix)

    # Since the portal url and remote url are same. We only need one function to handle portal access and git push
    def get_azure_devops_repo_url(self, repository_name):
        return construct_git_remote_url(
            organization_name=self._information.get_organization(),
            project_name=self._information.get_project(),
            repository_name=repository_name)

    # The function will initialize a git repo, create git remote, stage all changes and commit the code
    # Exceptions: GitOperationException
    def setup_local_git_repository(self, repository_name, remote_prefix):
        remote_name = construct_git_remote_name(
            organization_name=self._information.get_organization(),
            project_name=self._information.get_project(),
            repository_name=repository_name,
            remote_prefix=remote_prefix)
        remote_url = construct_git_remote_url(
            organization_name=self._information.get_organization(),
            project_name=self._information.get_project(),
            repository_name=repository_name)

        if not does_local_git_repository_exist():
            git_init()

        git_add_remote(remote_name, remote_url)
        git_stage_all()
        git_commit("Create function app with azure devops build. Remote repository url: {url}".format(url=remote_url))

    # The function will push the current context in local git repository to Azure Devops
    # Exceptions: GitOperationException
    def push_local_to_azure_devops_repository(self, repository_name, remote_prefix, force):
        remote_name = construct_git_remote_name(
            organization_name=self._information.get_organization(),
            project_name=self._information.get_project(),
            repository_name=repository_name,
            remote_prefix=remote_prefix)
        git_push(remote_name, force)
