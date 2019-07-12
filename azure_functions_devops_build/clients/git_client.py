# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.devops.v5_1.git.models import GitRepositoryCreateOptions
from ..base.base_client import BaseClient


class GitClient(BaseClient):

    def __init__(self, connection, information):
        super(GitClient, self).__init__(information)
        self._client = connection.clients.get_git_client()

    def create_repository(self, repository_name, project_obj=None):
        if not project_obj:
            raise ValueError("project_obj")

        if not repository_name:
            raise ValueError("repository_name")

        git_repo_options = GitRepositoryCreateOptions(
            name=repository_name,
            project=project_obj)

        return self._client.create_repository(git_repo_options, self.project)

    def get_repositories(self, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        return self._client.get_repositories(project=project_name)

    def get_repository_by_name(self, repository_name, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        if not repository_name:
            raise ValueError("repository_name")

        repositories = self._client.get_repositories(project=project_name)
        return next((r for r in repositories if r.name == repository_name), None)

    def get_branches(self, repository_name, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        if not repository_name:
            raise ValueError("repository_name")

        repositories = self._client.get_repositories(project=project_name)
        return next((r for r in repositories if r.name == repository_name), None)
