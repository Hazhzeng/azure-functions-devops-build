# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import json
import os
try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open(os.devnull, 'w')
from subprocess import check_output, CalledProcessError
from ..base.base_information import BaseInformation
from ..clients.client_factory import ClientFactory
from ..constants import SERVICE_ENDPOINT_DOMAIN
from ..exceptions import RoleAssignmentException


class ServiceEndpointManager(object):

    def __init__(self, organization_name="", project_name="", creds=None):
        self._information = BaseInformation(
            organization=organization_name,
            project=project_name,
            credential=creds)
        self._service_endpoint = ClientFactory.get_service_endpoint_client(self._information)

    # Get the details of a service endpoint
    # If endpoint does not exist, return an empty list
    def get_service_endpoints(self, repository_name):
        service_endpoint_name = self._get_service_endpoint_name(repository_name)
        return self._service_endpoint.get_service_endpoints_by_name(service_endpoint_name)

    # This function requires user permission of Microsoft.Authorization/roleAssignments/write
    # i.e. only the owner of the subscription can use this function
    def create_service_endpoint(self, repository_name):
        command = "az account show --o json"
        token_resp = check_output(command, shell=True).decode()
        account = json.loads(token_resp)

        # The following command requires Microsoft.Authorization/roleAssignments/write permission
        service_principle_name = self._get_service_endpoint_name(repository_name)

        # A service principal name has to include the http/https to be valid
        command = "az ad sp create-for-rbac --o json --name http://" + service_principle_name
        try:
            token_resp = check_output(command, stderr=DEVNULL, shell=True).decode()
        except CalledProcessError:
            raise RoleAssignmentException(command)

        token_resp_dict = json.loads(token_resp)

        return self._service_endpoint.create_service_endpoint(
            name=token_resp_dict['displayName'],
            subscription_id=account['id'],
            subscription_name=account['name'],
            tenant_id=token_resp_dict['tenant'],
            service_principal_id=token_resp_dict['appId'],
            service_principal_key=token_resp_dict['password'])

    def list_service_endpoints(self):
        """
        :rtype: [ int: azure.devops.v5_1.service_endpoint.models.ServiceEndpoint ]
        """
        return self._service_endpoint.get_service_endpoints()

    def _get_service_endpoint_name(self, repository_name):
        return "{domain}/{org}/{proj}/{repo}".format(
            domain=SERVICE_ENDPOINT_DOMAIN,
            org=self._information.get_organization(),
            proj=self._information.get_project(),
            repo=repository_name
        )
