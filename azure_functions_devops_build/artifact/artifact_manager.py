# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ..base.base_manager import BaseManager
from vsts.exceptions import VstsClientRequestError


class ArtifactManager(BaseManager):
    def __init__(self, organization_name, project_name, creds):
        super(ArtifactManager, self).__init__(
            creds,
            organization_name=organization_name,
            project_name=project_name)

    def list_artifacts(self, build_id):
        project = self._get_project_by_name(self._project_name)
        try:
            result = self._build_client.get_artifacts(build_id, project.id)
        except VstsClientRequestError:
            return []
        return result
