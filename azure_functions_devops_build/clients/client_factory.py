# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.devops.connection import Connection
from ..exceptions import (
    NoConnectionCredentialError,
    NoConnectionOrganzationError)
from .core_client import CoreClient
from .build_client import BuildClient
from .extension_management_client import ExtensionManagementClient
from .git_client import GitClient
from .release_client import ReleaseClient
from .service_endpoint_client import ServiceEndpointClient
from .task_agent_client import TaskAgentClient
from .github_client import GithubClient


class ClientFactory(object):

    _cached_core_client = None
    _cached_git_client = None
    _cached_extension_management_client = None
    _cached_build_client = None
    _cached_release_client = None
    _cached_service_endpoint_client = None
    _cached_task_agent_client = None
    _cached_github_client = None

    @classmethod
    def get_core_client(cls, information):
        if cls._cached_core_client is None:
            connection = cls._create_connection(information)
            cls._cached_core_client = CoreClient(connection, information)
        else:
            cls._cached_core_client.update_information(information)

        return cls._cached_core_client

    @classmethod
    def get_build_client(cls, information):
        if cls._cached_build_client is None:
            connection = cls._create_connection(information)
            cls._cached_build_client = BuildClient(connection, information)
        else:
            cls._cached_build_client.update_information(information)

        return cls._cached_build_client

    @classmethod
    def get_extension_management_client(cls, information):
        if cls._cached_extension_management_client is None:
            connection = cls._create_connection(information)
            cls._cached_extension_management_client = ExtensionManagementClient(connection, information)
        else:
            cls._cached_extension_management_client.update_information(information)

        return cls._cached_extension_management_client

    @classmethod
    def get_git_client(cls, information):
        if cls._cached_git_client is None:
            connection = cls._create_connection(information)
            cls._cached_git_client = GitClient(connection, information)
        else:
            cls._cached_git_client.update_information(information)

        return cls._cached_git_client

    @classmethod
    def get_release_client(cls, information):
        if cls._cached_release_client is None:
            connection = cls._create_connection(information)
            cls._cached_release_client = ReleaseClient(connection, information)
        else:
            cls._cached_release_client.update_information(information)

        return cls._cached_release_client

    @classmethod
    def get_service_endpoint_client(cls, information):
        if cls._cached_service_endpoint_client is None:
            connection = cls._create_connection(information)
            cls._cached_service_endpoint_client = ServiceEndpointClient(connection, information)
        else:
            cls._cached_service_endpoint_client.update_information(information)

        return cls._cached_service_endpoint_client

    @classmethod
    def get_task_agent_client(cls, information):
        if cls._cached_task_agent_client is None:
            connection = cls._create_connection(information)
            cls._cached_task_agent_client = TaskAgentClient(connection, information)
        else:
            cls._cached_task_agent_client.update_information(information)

        return cls._cached_task_agent_client

    @classmethod
    def get_github_client(cls, information):
        if cls._cached_github_client is None:
            connection = cls._create_connection(information)
            cls._cached_github_client = GithubClient(connection, information)
        else:
            cls._cached_github_client.update_information(information)

        return cls._cached_github_client

    @classmethod
    def _create_connection(cls, information):
        if not information.has_credential():
            raise NoConnectionCredentialError()

        if not information.has_organization():
            raise NoConnectionOrganzationError()

        return Connection(
            base_url='https://dev.azure.com/' + information.get_organization(),
            creds=information.get_credential())
