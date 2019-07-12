# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.devops.v5_1.service_endpoint.models import (
    EndpointAuthorization,
    ServiceEndpoint)
from ..base.base_client import BaseClient
from ..utils.service_endpoint_utils import sanitize_github_repository_fullname

class ServiceEndpointClient(BaseClient):

    def __init__(self, connection, information):
        super(ServiceEndpointClient, self).__init__(information)
        self._client = connection.clients.get_service_endpoint_client()

    def get_service_endpoints(self, endpoint_type=None, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        return self._client.get_service_endpoints(project=project_name, type=endpoint_type)

    def get_service_endpoints_by_name(self, name, endpoint_type=None, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        return self._client.get_service_endpoints_by_names(project_name, [name], endpoint_type)

    def create_github_service_endpoint(self, repository_fullname, github_pat=None, project_name=None):
        if github_pat is None:
            github_pat = self.github_pat

        if not github_pat:
            raise ValueError("github_pat")

        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        endpoint_authorization_obj = EndpointAuthorization(
            parameters={
                "accessToken": github_pat
            },
            scheme="PersonalAccessToken")
        service_endpoint_name = sanitize_github_repository_fullname(repository_fullname)
        service_endpoint_obj = ServiceEndpoint(
            administrators_group=None,
            authorization=endpoint_authorization_obj,
            data={},
            name=service_endpoint_name,
            type="github",
            url="http://github.com"
        )
        return self._client.create_service_endpoint(service_endpoint_obj, project_name)

    def create_service_endpoint(self, name, tenant_id, subscription_id, subscription_name,
                                service_principal_id, service_principal_key, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        data = {
            "subscriptionId": subscription_id,
            "subscriptionName": subscription_name,
            "environment": "AzureCloud",
            "scopeLevel": "Subscription"
        }

        auth = EndpointAuthorization(
            parameters={
                "tenantid": tenant_id,
                "serviceprincipalid": service_principal_id,
                "authenticationType": "spnKey",
                "serviceprincipalkey": service_principal_key
            },
            scheme="ServicePrincipal"
        )

        service_endpoint = ServiceEndpoint(
            administrators_group=None,
            authorization=auth,
            data=data,
            name=name,
            type="azurerm"
        )

        return self._client.create_service_endpoint(service_endpoint, project_name)
