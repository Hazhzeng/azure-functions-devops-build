# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import re
import logging
from msrest.service_client import ServiceClient
from msrest import Configuration, Deserializer
from msrest.exceptions import HttpOperationError

from ..user.user_manager import UserManager
from . import models


class OrganizationManager():
    """ Manage DevOps organizations

    Create or list existing organizations

    Attributes:
        config: url configuration
        client: authentication client
        dserialize: deserializer to process http responses into python classes
    """

    msa_organization_names = set()

    def __init__(self, base_url='https://app.vssps.visualstudio.com', creds=None,
                 create_organization_url='https://app.vsaex.visualstudio.com'):
        """Inits OrganizationManager"""
        self._creds = creds
        self._config = Configuration(base_url=base_url)
        self._client = ServiceClient(creds, self._config)
        #need to make a secondary client for the creating organization as it uses a different base url
        self._create_organization_config = Configuration(base_url=create_organization_url)
        self._create_organization_client = ServiceClient(creds, self._create_organization_config)

        self._list_region_config = Configuration(base_url='https://aex.dev.azure.com')
        self._list_region_client = ServiceClient(creds, self._create_organization_config)
        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self._deserialize = Deserializer(client_models)
        self._user_mgr = UserManager(creds=self._creds)

    @classmethod
    def is_msa_organization(cls, organization_name):
        if organization_name is None:
            return False

        return organization_name.lower() in cls.msa_organization_names

    def validate_organization_name(self, organization_name):
        """Validate an organization name by checking it does not already exist and that it fits name restrictions"""
        if organization_name is None:
            return models.ValidateAccountName(valid=False, message="The organization_name cannot be None")

        if re.search("[^0-9A-Za-z-]", organization_name):
            return models.ValidateAccountName(valid=False, message="""The name supplied contains forbidden characters.
                                                                      Only alphanumeric characters and dashes are allowed.
                                                                      Please try another organization name.""")
        #construct url
        url = '/_AzureSpsAccount/ValidateAccountName'

        #construct query parameters
        query_paramters = {}
        query_paramters['accountName'] = organization_name

        #construct header parameters
        header_paramters = {}
        header_paramters['Accept'] = 'application/json'

        request = self._client.get(url, params=query_paramters)
        response = self._client.send(request, headers=header_paramters)

        # Handle Response
        deserialized = None
        if response.status_code // 100 != 2:
            logging.error("GET %s", request.url)
            logging.error("response: %s", response.status_code)
            logging.error(response.text)
            raise HttpOperationError(self._deserialize, response)
        else:
            deserialized = self._deserialize('ValidateAccountName', response)

        return deserialized

    def list_organizations(self):
        """List what organizations this user is part of"""
        organizations_aad = self._list_organizations_request(self._user_mgr.aad_id, msa=False)
        organizations_msa = self._list_organizations_request(self._user_mgr.msa_id, msa=True)

        # Mark aad organizations as force_msa_pass_through = False
        organizations = organizations_aad
        aad_organization_ids = set([o.accountId for o in organizations.value])

        # Merge msa organizations
        for msa_org in organizations_msa.value:
            if msa_org.accountId not in aad_organization_ids:
                organizations.value.append(msa_org)
                self.__class__.msa_organization_names.add(msa_org.accountName.lower())

        # Summarize number of organizations
        organizations.count = len(organizations.value)
        return organizations

    def _list_organizations_request(self, member_id, msa):
        url = '/_apis/accounts'

        request = self._client.get(url, params={
            'api-version': '5.0-preview.1',
            'memberId': member_id
        })
        response = self._client.send(request, headers={
            'Authorization': 'Bearer {}'.format(self._user_mgr.get_access_token()),
            'X-VSS-ForceMsaPassThrough': 'true' if msa else 'false',
            'Accept': 'application/json'
        })

        # Handle Response
        deserialized = None
        if response.status_code // 100 != 2:
            logging.error("GET %s", request.url)
            logging.error("response: %s", response.status_code)
            logging.error(response.text)
            raise HttpOperationError(self._deserialize, response)
        else:
            deserialized = self._deserialize('Organizations', response)
        return deserialized

    def create_organization(self, region_code, organization_name):
        """Create a new organization for user"""
        url = '/_apis/HostAcquisition/collections'

        #construct query parameters
        query_paramters = {}
        query_paramters['collectionName'] = organization_name
        query_paramters['preferredRegion'] = region_code
        query_paramters['api-version'] = '4.0-preview.1'

        #construct header parameters
        header_paramters = {}
        header_paramters['Accept'] = 'application/json'
        header_paramters['Content-Type'] = 'application/json'
        if self._user_mgr.is_msa_account():
            header_paramters['X-VSS-ForceMsaPassThrough'] = 'true'

        #construct the payload
        payload = {}
        payload['VisualStudio.Services.HostResolution.UseCodexDomainForHostCreation'] = 'true'

        request = self._create_organization_client.post(url=url, params=query_paramters, content=payload)
        response = self._create_organization_client.send(request, headers=header_paramters)

        # Handle Response
        deserialized = None
        if response.status_code // 100 != 2:
            logging.error("GET %s", request.url)
            logging.error("response: %s", response.status_code)
            logging.error(response.text)
            raise HttpOperationError(self._deserialize, response)
        else:
            deserialized = self._deserialize('NewOrganization', response)

        return deserialized

    def list_regions(self):
        """List what regions organizations can exist in"""

        # Construct URL
        url = '/_apis/hostacquisition/regions'

        #construct header parameters
        header_paramters = {}
        header_paramters['Accept'] = 'application/json'

        # Construct and send request
        request = self._list_region_client.get(url, headers=header_paramters)
        response = self._list_region_client.send(request)

        # Handle Response
        deserialized = None
        if response.status_code // 100 != 2:
            logging.error("GET %s", request.url)
            logging.error("response: %s", response.status_code)
            logging.error(response.text)
            raise HttpOperationError(self._deserialize, response)
        else:
            deserialized = self._deserialize('Regions', response)

        return deserialized

    def close_connection(self):
        """Close the sessions"""
        self._client.close()
        self._create_organization_client.close()
