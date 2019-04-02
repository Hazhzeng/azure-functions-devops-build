# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ..base.base_github_manager import BaseGithubManager

class GithubRepositoryManager(BaseGithubManager):

    def check_github_repository(self, repository_fullname):
        header_parameters = self.construct_github_request_header()
        request = self._client.get('/repos/{repo}'.format(repo=repository_fullname))
        response = self._client.send(request, header_parameters)
        if response.status_code // 100 == 2:
            return True
        return False
