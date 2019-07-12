# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest.service_client import ServiceClient
from msrest import Configuration
from msrest.exceptions import HttpOperationError
from ..base.base_client import BaseClient
from ..utils.model_utils import ModelUtils


class UserClient(BaseClient):

    def __init__(self, information):
        super(UserClient, self).__init__(information)
        self._config = Configuration(base_url='https://peprodscussu2.portalext.visualstudio.com')
        self._client = ServiceClient(self.credential, self._config)

        # create cache for two user type
        self._cache_aad_user = None
        self._cache_msa_user = None

    def is_msa_account(self):
        user_id_aad = self.get_user(msa=False).id
        user_id_msa = self.get_user(msa=True).id
        return user_id_aad != user_id_msa

    def get_user(self, msa=False):
        # Try to get from cache
        if msa is True and self._cache_msa_user is not None:
            return self._cache_msa_user
        if msa is False and self._cache_aad_user is not None:
            return self._cache_aad_user

        header_parameters = {}
        header_parameters['X-VSS-ForceMsaPassThrough'] = 'true' if msa else 'false'
        header_parameters['Accept'] = 'application/json'
        request = self._client.get('/_apis/AzureTfs/UserContext')
        response = self._client.send(request, header_parameters)

        if response.status_code // 100 != 2:
            deserialized = ModelUtils.deserialize_response('User', response)
        else:
            raise HttpOperationError(ModelUtils.get_deserializer(), response)

        # Write to cache
        if msa is True and self._cache_msa_user is None:
            self._cache_msa_user = deserialized
        if msa is False and self._cache_aad_user is None:
            self._cache_aad_user = deserialized

        return deserialized

    @property
    def aad_id(self):
        return self.get_user(msa=False).id

    @property
    def msa_id(self):
        return self.get_user(msa=True).id
