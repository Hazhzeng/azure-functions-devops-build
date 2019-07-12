# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import time
import logging
from msrest.service_client import ServiceClient
from msrest import Configuration, Deserializer
from msrest.exceptions import HttpOperationError
from vsts.exceptions import VstsServiceError
import vsts.core.v4_1.models.team_project as team_project
from ..user.user_manager import UserManager
from ..base.base_manager import BaseManager
from ..organization.organization_manager import OrganizationManager
from . import models


class ProjectManager(BaseManager):
    """ Manage DevOps projects

    Create or list existing projects

    Attributes:
        config: url configuration
        client: authentication client
        dserialize: deserializer to process http responses into python classes
        Otherwise see BaseManager
    """

    def __init__(self, base_url='https://dev.azure.com/{}', organization_name="", creds=None,
                 create_project_url='https://dev.azure.com'):
        """Inits Project as per BaseManager and adds relevant other needed fields"""
        super(ProjectManager, self).__init__(creds, organization_name=organization_name)
        base_url = base_url.format(organization_name)
        self._config = Configuration(base_url=base_url)
        self._client = ServiceClient(creds, self._config)
        self._credentials = creds
        self._organization_name = organization_name
        # Need to make a secondary client for the creating project as it uses a different base url
        self._create_project_config = Configuration(base_url=create_project_url)
        self._create_project_client = ServiceClient(creds, self._create_project_config)
        client_models = {k: v for k, v in models.__dict__.items() if isinstance(v, type)}
        self._deserialize = Deserializer(client_models)
        self._user_mgr = UserManager(creds=self._creds)

    def create_project(self, projectName):
        url = '/_apis/projects'

        is_msa = OrganizationManager.is_msa_organization(self._organization_name)
        print("is_msa: " + str(is_msa))
        request = self._client.post(url, params={
            'api-version': '5.0'
        })
        response = self._client.send(request, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-VSS-ForceMsaPassThrough': 'true' if is_msa else 'false'
        }, content={
            'name': projectName,
            'description': 'Azure Functions Devops Build created project',
            'capabilities': {
                'versioncontrol': {
                    'sourceControlType': 'Git',
                },
                'processTemplate': {
                    'templateTypeId': 'adcc42ab-9882-485e-a3ed-7678f01f66bc'
                }
            },
        })

        if response.status_code // 100 != 2:
            return models.ProjectFailed('Failed to create project')

        time.sleep(5)
        projects = self.list_projects()
        p = [p for p in projects.value if p.name.lower() == projectName.lower()]
        if not p:
            return models.ProjectFailed('Failed to find created project')

        project = p[0]
        project.valid = True
        return project

    def list_projects(self):
        """Lists the current projects within an organization"""

        # First pass without X-VSS-ForceMsaPassThrough header
        response = self._list_projects_request()

        deserialized = None
        if response.status_code == 203:
            return models.Projects(count=0, value=[])
        elif response.status_code == 200:
            deserialized = self._deserialize('Projects', response)
            return deserialized

        logging.error("GET %s", response.url)
        logging.error("response: %s", response.status_code)
        logging.error(response.text)
        raise HttpOperationError(self._deserialize, response)

    def _list_projects_request(self):
        url = '/_apis/projects'

        is_msa = OrganizationManager.is_msa_organization(self._organization_name)
        print("is_msa: " + str(is_msa))
        request = self._client.get(url, params={
            'includeCapabilities': 'true',
            'api-version': '5.0'
        })
        response = self._client.send(request, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-VSS-ForceMsaPassThrough': 'true' if is_msa else 'false'
        })
        return response

    def _poll_project(self, project_id):
        """Helper function to poll the project"""
        project_created = False
        while not project_created:
            time.sleep(1)
            res = self._is_project_created(project_id)
            logging.info('project creation is: %s', res.status)
            if res.status == 'succeeded':
                project_created = True

    def _is_project_created(self, project_id):
        """Helper function to see the status of a project"""
        url = '/' + self._organization_name + '/_apis/operations/' + project_id

        is_msa = OrganizationManager.is_msa_organization(self._organization_name)

        request = self._create_project_client.get(url, params={})
        response = self._create_project_client.send(request, headers={
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-VSS-ForceMsaPassThrough': 'true' if is_msa else 'false'
        })

        # Handle Response
        deserialized = None
        if response.status_code // 100 != 2:
            logging.error("GET %s", request.url)
            logging.error("response: %s", response.status_code)
            logging.error(response.text)
            raise HttpOperationError(self._deserialize, response)
        else:
            deserialized = self._deserialize('ProjectPoll', response)

        return deserialized
