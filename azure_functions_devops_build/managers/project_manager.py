# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import time
from ..base.base_information import BaseInformation
from ..clients.client_factory import ClientFactory
from ..models import ProjectFailed


class ProjectManager(object):

    def __init__(self, organization_name="", creds=None):
        self._information = BaseInformation(
            credential=creds,
            organization=organization_name)
        self._devops_rest = ClientFactory.get_devops_rest_client(self._information)

    def create_project(self, project_name):
        self._devops_rest.create_project(
            msa=False,
            project_name=project_name)

        time.sleep(2)
        projects = self.list_projects()
        p = [p for p in projects.value if p.name.lower() == project_name.lower()]
        if not p:
            return ProjectFailed('Failed to find created project')

        project = p[0]
        project.valid = True
        return project

    def list_projects(self):
        return self._devops_rest.list_projects(msa=False)

    def _poll_project(self, project_id):
        project_created = False
        while not project_created:
            time.sleep(1)
            res = self._is_project_created(project_id)
            if res.status == 'succeeded':
                project_created = True

    def _is_project_created(self, project_id):
        return self._devops_rest.poll_project_by_id(
            msa=False,
            project_id=project_id)
