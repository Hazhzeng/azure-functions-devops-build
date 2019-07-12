# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest import Configuration
from msrest.exceptions import HttpOperationError
from msrest.service_client import ServiceClient
from azure.devops.v5_1.task_agent.models import TaskAgentPool
from ..base.base_client import BaseClient
from ..utils.model_utils import ModelUtils


class DevopsRestClient(BaseClient):

    def __init__(self, information):
        super(DevopsRestClient, self).__init__(information)
        self._organization_client = ServiceClient(
            self.credential,
            Configuration(base_url='https://dev.azure.com/{}/{}'.format(self.organization, self.project)))
        self._project_client = ServiceClient(
            self.credential,
            Configuration(base_url='https://dev.azure.com/{}'.format(self.organization)))

    def get_pool_by_name(self, msa, name):
        url = '/_apis/distributedtask/queues'

        request = self._project_client.get(url, params={
            'actionFilter': '16',
            'poolName': name,
            'api-version': '5.0-preview.1'
        })
        response = self._project_client.send(request, headers={
            'Accept': 'application/json',
            'X-VSS-ForceMsaPassThrough': 'true' if msa else 'false'
        })

        if response.status_code // 100 == 2:
            return ModelUtils.deserialize_response(TaskAgentPool, response)

        raise HttpOperationError(ModelUtils.get_deserializer(), response)

    def list_pools(self, msa):
        url = '/_apis/distributedtask/queues'

        request = self._project_client.get(url, params={
            'actionFilter': '16',
            'api-version': '5.0-preview.1'
        })
        response = self._project_client.send(request, headers={
            'Accept': 'application/json',
            'X-VSS-ForceMsaPassThrough': 'true' if msa else 'false'
        })

        if response.status_code // 100 == 2:
            return ModelUtils.deserialize_response('Pools', response)

        raise HttpOperationError(ModelUtils.get_deserializer(), response)

    def list_projects(self, msa):
        url = '/_apis/projects'

        request = self._organization_client.get(url, params={
            'api-version': '5.0'
        })
        response = self._organization_client.send(request, headers={
            'includeCapabilities': 'true',
            'X-VSS-ForceMsaPassThrough': 'true' if msa else 'false'
        })

        if response.status_code // 100 == 2:
            return ModelUtils.deserialize_response('Projects', response)

        raise HttpOperationError(ModelUtils.get_deserializer(), response)

    def poll_project_by_id(self, msa, project_id):
        url = '/_apis/operations/' + project_id

        request = self._organization_client.get(url, params={
            'api-version': '5.0'
        })
        response = self._organization_client.send(request, headers={
            'Accept': 'application/json',
            'X-VSS-ForceMsaPassThrough': 'true' if msa else 'false'
        })

        if response.status_code // 100 == 2:
            return ModelUtils.deserialize_response('ProjectPoll', response)

        raise HttpOperationError(ModelUtils.get_deserializer(), response)

    def create_project(self, msa, project_name):
        url = '/_apis/projects'

        request = self._organization_client.post(url, params={
            'api-version': '5.0'
        })
        response = self._organization_client.send(request, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-VSS-ForceMsaPassThrough': 'true' if msa else 'false'
        }, content={
            'name': project_name,
            'description': 'Azure Functions Devops Build created project',
            'capabilities': {
                'versioncontrol': {
                    'sourceControlType': 'Git',
                },
                'processTemplate': {
                    'templateTypeId': 'adcc42ab-9882-485e-a3ed-7678f01f66bc'
                }
            },
        })
        if response.status_code // 100 == 2:
            return ModelUtils.deserialize_response('OperationReference', response)

        raise HttpOperationError(ModelUtils.get_deserializer(), response)
