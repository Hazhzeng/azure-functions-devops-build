# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ..base.base_client import BaseClient


class ReleaseClient(BaseClient):

    def __init__(self, connection, information):
        super(ReleaseClient, self).__init__(information)
        self._client = connection.clients.get_git_client()
