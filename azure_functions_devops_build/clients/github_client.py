# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest.service_client import ServiceClient
from msrest import Configuration
from ..base.base_client import BaseClient
from ..exceptions import GithubIntegrationRequestError


class GithubClient(BaseClient):

    def __init__(self, information):
        super(GithubClient, self).__init__(information)
        self._config = Configuration(base_url='https://api.github.com')
        self._client = ServiceClient(None, self._config)

    def check_github_pat(self, pat):
        request = self._client.get('/')
        response = self._client.send(request, self._construct_request_header(pat))
        if response.status_code // 100 == 2:
            return True
        return False

    def check_if_repository_exists(self, repository_fullname):
        request = self._client.get('/repos/{repo}'.format(repo=repository_fullname))
        response = self._client.send(request, self._construct_request_header())
        return response.status_code // 100 == 2

    def check_if_file_exists(self, repository_fullname, file_path):
        request = self._client.get('/repos/{repo}/contents/{path}'.format(
            repo=repository_fullname,
            path=file_path))
        response = self._client.send(request, self._construct_request_header())
        return response.status_code // 100 == 2

    def get_file_content(self, repository_fullname, file_path, get_metadata):
        header_parameters = self._construct_request_header()

        if get_metadata:  # Get files metadata
            header_parameters['Content-Type'] = 'application/json'
        else:  # Get files content
            header_parameters['Accept'] = 'application/vnd.github.v3.raw'

        request = self._client.get('/repos/{repo}/contents/{path}'.format(
            repo=repository_fullname,
            path=file_path
        ))
        response = self._client.send(request, header_parameters)
        if response.status_code // 100 == 2:
            return response.json()

        raise GithubIntegrationRequestError(response.status_code)

    def put_file_content(self, repository_fullname, file_path, data):
        header_parameters = self._construct_request_header()
        header_parameters['Content-Type'] = 'application/json'
        request = self._client.put(
            url='/repos/{repo}/contents/{path}'.format(repo=repository_fullname, path=file_path),
            headers=header_parameters,
            content=data
        )
        response = self._client.send(request)
        if response.status_code // 100 == 2:
            return response

        raise GithubIntegrationRequestError(response.status_code)

    def _construct_request_header(self, pat=None):
        headers = {
            "Accept": "application/vnd.github.v3+json"
        }

        if pat is None:
            pat = self.github_pat

        headers["Authorization"] = "token {pat}".format(pat=pat)
        return headers
