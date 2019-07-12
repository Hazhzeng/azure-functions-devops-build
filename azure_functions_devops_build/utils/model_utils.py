# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from msrest import Deserializer
from .. import models


class ModelUtils(object):
    client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
    client_deserializer = Deserializer(client_models)

    @classmethod
    def deserialize_response(cls, attr, obj):
        return cls.client_deserializer(attr, obj)

    @classmethod
    def get_deserializer(cls):
        return cls.client_deserializer
