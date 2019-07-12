# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest.service_client import ServiceClient
from msrest import Configuration
from msrest.exceptions import HttpOperationError
from ..base.base_client import BaseClient
from ..utils.model_utils import ModelUtils


class OrganizationListingClient(BaseClient):

    def __init__(self, information):
        super(OrganizationListingClient, self).__init__(information)
        self._config = Configuration(base_url='https://app.vssps.visualstudio.com')
        self._client = ServiceClient(self.credential, self._config)

    def validate_organization_name(self, organization_name=None):
        if organization_name is None:
            organization_name = self.organization

        if not organization_name:
            raise ValueError("organization_name")

        url = '/_AzureSpsAccount/ValidateAccountName'

        request = self._client.get(url, params={
            'accountName': organization_name
        })
        response = self._client.send(request, headers={
            'Accept': 'application/json'
        })

        if response.status_code // 100 == 2:
            return ModelUtils.deserialize_response('ValidateAccountName', response)

        raise HttpOperationError(ModelUtils.get_deserializer(), response)

    def list_organizations(self, member_id, msa):
        url = '/_apis/Accounts'

        request = self._client.get(url, params={
            'memberId': member_id,
            'includeMSAAccounts': True,
            'inlcudeDisabledAccounts': False,
            'queryOnlyOwnerAccounts': True,
            'providerNamespaceId': 'VisualStudioOnline',
            'api-version': '5.0'
        })
        response = self._client.send(request, headers={
            'X-VSS-ForceMsaPassThrough': 'true' if msa else 'false',
            'Accept': 'application/json'
        })

        if response.status_code // 100 == 2:
            return ModelUtils.deserialize_response('Organizations', response)

        raise HttpOperationError(ModelUtils.get_deserializer(), response)
