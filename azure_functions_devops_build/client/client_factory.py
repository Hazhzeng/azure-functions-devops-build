# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.devops.connection import Connection
from ..base.base_information import BaseInformation


class ClientFactory(BaseInformation):

    _cached_core_client = None
    _cached_git_client = None
    _cached_extmanagement_client = None
    _cached_build_client = None
    _cached_release_client = None
    _cached_serviceendpoint_client = None

    @classmethod
    def get_core_client(cls):
        if cls._cached_core_client is None:
            cls._cached_core_client =
        return cls._cached_core_client
