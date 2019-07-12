# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ..base.base_information import BaseInformation
from ..clients.client_factory import ClientFactory
from ..utils.service_endpoint_utils import sanitize_github_repository_fullname


class GithubServiceEndpointManager(object):

    def __init__(self, organization_name=None, project_name=None, creds=None):
        self._information = BaseInformation(
            credential=creds,
            project=project_name,
            organization=organization_name)
        self._service_endpoint = ClientFactory.get_service_endpoint_client(self._information)

    def get_github_service_endpoints(self, repository_fullname):
        service_endpoint_name = sanitize_github_repository_fullname(repository_fullname)
        return self._service_endpoint.get_service_endpoints_by_name(
            name=service_endpoint_name,
            endpoint_type="github")

    def create_github_service_endpoint(self, repository_fullname, github_pat):
        return self._service_endpoint.create_github_service_endpoint(repository_fullname, github_pat)
