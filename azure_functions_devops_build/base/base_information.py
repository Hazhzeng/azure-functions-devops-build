# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


class BaseInformation(object):

    _credential = None
    _organization = None
    _project = None
    _repository = None
    _pool = None

    @classmethod
    def add_or_update_credential(cls, credential):
        cls._credential = credential

    @classmethod
    def has_credential(cls):
        return bool(cls._credential)

    @classmethod
    def add_or_update_organization(cls, organization):
        cls._organization = organization

    @classmethod
    def has_organization(cls):
        return bool(cls._organization)

    @classmethod
    def add_or_update_project(cls, project):
        cls._project = project

    @classmethod
    def has_project(cls):
        return bool(cls._project)

    @classmethod
    def add_or_update_repository(cls, repository):
        cls._repository = repository

    @classmethod
    def has_repository(cls):
        return bool(cls._repository)

    @classmethod
    def add_or_update_pool(cls, pool):
        cls._pool = pool

    @classmethod
    def has_pool(cls):
        return bool(cls._pool)