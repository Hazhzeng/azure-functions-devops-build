# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ..base.base_information import BaseInformation
from ..clients.client_factory import ClientFactory
from ..utils.service_endpoint_utils import sanitize_github_repository_fullname

class GithubServiceEndpointManager(object):
    def __init__(self, organization_name, project_name, creds):
        self._information = BaseInformation(
            credential=creds,
            project=project_name,
            organization=organization_name)
        self._service_endpoint = ClientFactory.get_service_endpoint_client(self._information)

    def get_github_service_endpoints(self, repository_fullname):
        service_endpoint_name = sanitize_github_repository_fullname(repository_fullname)
        try:
            result = self._service_endpoint.get_service_endpoints_by_names(
                self._project_name,
                [service_endpoint_name],
                type="github"
            )
        except VstsServiceError:
            return []
        return result

    def create_github_service_endpoint(self, repository_fullname, github_pat):
        data = {}
        auth = models.endpoint_authorization.EndpointAuthorization(
            parameters={
                "accessToken": github_pat
            },
            scheme="PersonalAccessToken"
        )
        service_endpoint_name = self.sanitize_github_repository_fullname(repository_fullname)
        service_endpoint = models.service_endpoint.ServiceEndpoint(
            administrators_group=None,
            authorization=auth,
            data=data,
            name=service_endpoint_name,
            type="github",
            url="http://github.com"
        )

        return self._service_endpoint_client.create_service_endpoint(service_endpoint, self._project_name)