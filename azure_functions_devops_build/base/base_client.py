# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

class BaseClient(object):

    def __init__(self, information):
        self._information = information

    def update_information(self, new_information):
        if new_information.has_credential():
            self._information.add_or_update_credential(
                new_information.get_credential())

        if new_information.has_organization():
            self._information.add_or_update_organization(
                new_information.get_organization())

        if new_information.has_project():
            self._information.add_or_update_project(
                new_information.get_project())

        if new_information.has_repository():
            self._information.add_or_update_repository(
                new_information.get_repository())

        if new_information.has_pool():
            self._information.add_or_update_pool(
                new_information.get_pool())

    @property
    def organization(self):
        return self._information.get_organization()

    @property
    def project(self):
        return self._information.get_project()

    @property
    def repository(self):
        return self._information.get_repository()

    @property
    def github_pat(self):
        return self._information.get_github_pat()

    @property
    def credential(self):
        return self._information.get_credential()
