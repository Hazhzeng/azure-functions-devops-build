# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ..base.base_information import BaseInformation
from ..clients.client_factory import ClientFactory


class ArtifactManager(object):
    def __init__(self, organization_name=None, project_name=None, creds=None):
        self._information = BaseInformation(
            credential=creds,
            organization=organization_name,
            project=project_name)
        self._build = ClientFactory.get_build_client(self._information)

    def list_artifacts(self, build_id):
        """
        :rtype: [azure.devops.v5_1.build.models.BuildArtifact]
        """
        return self._build.get_artifacts(build_id)
