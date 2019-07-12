# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ..base.base_information import BaseInformation
from ..clients.client_factory import ClientFactory


class PoolManager(object):
    def __init__(self, creds=None, organization_name="", project_name=""):
        self._information = BaseInformation(
            credential=creds,
            organization=organization_name,
            project=project_name)
        self._devops_rest = ClientFactory.get_devops_rest_client(self._information)

    def list_pools(self):
        return self._devops_rest.list_pools(msa=False)
