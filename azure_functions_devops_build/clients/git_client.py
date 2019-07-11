# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ..base.base_client import BaseClient


class GitClient(BaseClient):

    def __init__(self, connection, information):
        super(GitClient, self).__init__(information)
        self._client = connection.clients.get_git_client()

    def get_repository_by_name(self, repository_name, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        if not repository_name:
            raise ValueError("repository_name")

        repositories = self._client.get_repositories(project=project_name)
        return next((r for r in repositories if r.name == repository_name), None)
