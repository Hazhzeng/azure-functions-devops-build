# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ..base.base_client import BaseClient


class TaskAgentClient(BaseClient):

    def __init__(self, connection, information):
        super(TaskAgentClient, self).__init__(information)
        self._client = connection.clients.get_task_agent()

    def get_agent_pool_by_name(self, pool_name):
        pools = self._client.get_agent_pools(pool_name=pool_name)
        if not pools:
            return None
        return pools[0]
