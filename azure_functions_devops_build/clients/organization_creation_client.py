# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest import Configuration
from msrest.exceptions import HttpOperationError
from msrest.service_client import ServiceClient
from ..base.base_client import BaseClient
from ..utils.model_utils import ModelUtils


class OrganizationCreationClient(BaseClient):

    def __init__(self, information):
        super(OrganizationCreationClient, self).__init__(information)
        self._config = Configuration(base_url='https://app.vsaex.visualstudio.com')
        self._client = ServiceClient(self.credential, self._config)

    def create_organization(self, region_code, msa, organization_name=None):
        url = '/_apis/Accounts'

        if organization_name is None:
            organization_name = self.organization

        if not organization_name:
            raise ValueError('organization_name')

        request = self._client.post(url=url, params={
            'collectionName': organization_name,
            'preferredRegion': region_code,
            'api-version': '5.0'
        }, content={
            'VisualStudio.Services.HostResolution.UseCodexDomainForHostCreation': 'true'
        })
        response = self._client.send(request, headers={
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-VSS-ForceMsaPassThrough': 'true' if msa else 'false'
        })

        if response.status_code // 100 == 2:
            return ModelUtils.deserialize_response('NewOrganization', response)

        raise HttpOperationError(ModelUtils.get_deserializer(), response)
