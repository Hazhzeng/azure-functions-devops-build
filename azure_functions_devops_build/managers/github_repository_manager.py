# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import base64
from ..base.base_information import BaseInformation
from ..clients.client_factory import ClientFactory
from ..exceptions import (
    GithubIntegrationRequestError,
    GithubContentNotFound,
    GithubUnauthorizedError)


class GithubRepositoryManager(object):

    def __init__(self, pat=None):
        self._information = BaseInformation(github_pat=pat)
        self._github = ClientFactory.get_github_client(self._information)

    def check_github_repository(self, repository_fullname):
        return self._github.check_if_repository_exists(repository_fullname)

    def check_github_file(self, repository_fullname, file_path):
        return self._github.check_if_file_exists(repository_fullname, file_path)

    def get_content(self, repository_fullname, file_path, get_metadata=True):
        try:
            result = self._github.get_file_content(repository_fullname, file_path, get_metadata)
        except GithubIntegrationRequestError as gire:
            if gire.message == 401:
                raise GithubUnauthorizedError('Failed to write {repo}/{path}'.format(
                    repo=repository_fullname,
                    path=file_path
                ))
            if gire.message == 404:
                raise GithubContentNotFound('Failed to find {repo}/{path}'.format(
                    repo=repository_fullname,
                    path=file_path
                ))
            raise GithubIntegrationRequestError(str(gire.message))
        return result

    def put_content(self, repository_fullname, file_path, data):
        try:
            result = self._github.put_file_content(repository_fullname, file_path, data)
        except GithubIntegrationRequestError as gire:
            if gire.message == 401:
                raise GithubUnauthorizedError('Failed to write {repo}/{path}'.format(
                    repo=repository_fullname,
                    path=file_path
                ))
            if gire.message == 404:
                raise GithubContentNotFound('Failed to find {repo}/{path}'.format(
                    repo=repository_fullname,
                    path=file_path
                ))
            raise GithubIntegrationRequestError(str(gire.message))
        return result

    def commit_file(self, repository_fullname, file_path, commit_message, file_data, sha=None, encode='utf-8'):
        data = {
            "branch": "master",
            "message": "{message}".format(message=commit_message),
            "content": base64.b64encode(bytes(file_data.encode(encode))).decode('ascii'),
        }

        if sha:
            data["sha"] = sha

        return self.put_content(
            repository_fullname=repository_fullname,
            file_path=file_path,
            data=data
        )
