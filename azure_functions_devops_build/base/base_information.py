# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


class BaseInformation(object):

    def __init__(
            self,
            credential=None,
            organization=None,
            project=None,
            repository=None,
            pool=None,
            github_pat=None
    ):
        self._credential = credential
        self._organization = organization
        self._project = project
        self._repository = repository
        self._pool = pool
        self._github_pat = github_pat

    def add_or_update_credential(self, credential):
        self._credential = credential

    def has_credential(self):
        return bool(self._credential)

    def get_credential(self):
        return self._credential

    def add_or_update_organization(self, organization):
        self._organization = organization

    def has_organization(self):
        return bool(self._organization)

    def get_organization(self):
        return self._organization

    def add_or_update_project(self, project):
        self._project = project

    def has_project(self):
        return bool(self._project)

    def get_project(self):
        return self._project

    def add_or_update_repository(self, repository):
        self._repository = repository

    def has_repository(self):
        return bool(self._repository)

    def get_repository(self):
        return self._repository

    def add_or_update_pool(self, pool):
        self._pool = pool

    def has_pool(self):
        return bool(self._pool)

    def get_pool(self):
        return self._pool

    def add_or_update_github_pat(self, github_pat):
        self._github_pat = github_pat

    def has_github_pat(self):
        return bool(self._github_pat)

    def get_github_pat(self):
        return self._github_pat
