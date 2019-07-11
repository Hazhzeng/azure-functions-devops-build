# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ..base.base_client import BaseClient


class ExtensionManagementClient(BaseClient):

    def __init__(self, connection, information):
        super(ExtensionManagementClient, self).__init__(information)
        self._client = connection.clients.get_extension_management_client()

    def list_extensions(self):
        return self._client.get_installed_extensions()

    def install_extension(self, publisher, name):
        return self._client.install_extension_by_name(publisher, name)
