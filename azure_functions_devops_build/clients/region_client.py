# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest import Configuration
from msrest.service_client import ServiceClient
from msrest.exceptions import HttpOperationError
from ..base.base_client import BaseClient
from ..models import Regions
from ..utils.model_utils import ModelUtils


class RegionClient(BaseClient):

    def __init__(self, information):
        super(RegionClient, self).__init__(information)
        self._config = Configuration(base_url='https://aex.dev.azure.com')
        self._client = ServiceClient(self.credential, self._config)

    def list_regions(self):
        url = '/_apis/hostacquisition/regions'

        request = self._client.get(url, headers={
            'Accept': 'application/json'
        })
        response = self._client.send(request)

        if response.status_code // 100 == 2:
            return ModelUtils.deserialize_response(Regions, response)

        raise HttpOperationError(ModelUtils.get_deserializer(), response)
