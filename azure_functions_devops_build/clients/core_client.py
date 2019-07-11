# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ..base.base_client import BaseClient


class CoreClient(BaseClient):

    def __init__(self, connection, information):
        super(CoreClient, self).__init__(information)
        self._client = connection.clients.get_core_client()

    def get_project_by_name(self, project_name=None):
        """
        :type project_name: str
        """
        projects = self._client.get_projects()

        if project_name is None:
            project_name = self._information.get_project()

        return next((p for p in projects if p.name == project_name), None)
