# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.devops.v5_1.release.models import ReleaseStartMetadata
from ..base.base_client import BaseClient


class ReleaseClient(BaseClient):

    def __init__(self, connection, information):
        super(ReleaseClient, self).__init__(information)
        self._client = connection.clients.get_git_client()

    def create_release_definition(self, release_definition, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        return self._client.create_release_definition(release_definition, project_name)

    def create_release(self, definition_id, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        release_start_metadata = ReleaseStartMetadata(
            definition_id=definition_id,
            is_draft=False,
            properties={"ReleaseCreationSource": "ReleaseHub"})

        return self._client.create_release(release_start_metadata, project_name)

    def get_release_definitions(self, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        return self._client.get_release_definitions(project_name)

    def get_release_definition_by_name(self, name, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        releases = self._client.get_release_definitions(project_name)
        return next((r for r in releases if r.name == name), None)

    def get_releases_by_definition_id(self, definition_id, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        return self._client.get_release_definitions(
            project=project_name,
            definition_id=definition_id)

    def get_releases(self, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        return self._client.get_releases(project_name)
