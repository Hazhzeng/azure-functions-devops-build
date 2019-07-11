# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.devops.v5_1.build.models import (
    AgentPoolQueue,
    BuildRepository,
    TeamProjectReference,
    BuildDefinition,
    DefinitionReference,
    Build)
from ..base.base_client import BaseClient
from ..utils.builder_utils import get_build_process, get_build_triggers
from ..exceptions import (
    BuildErrorException)


class BuildClient(BaseClient):

    def __init__(self, connection, information):
        super(BuildClient, self).__init__(information)
        self._client = connection.clients.get_build_client()

    def create_build(self, pool_obj, project_obj, build_definition_obj):
        team_project_reference_obj = TeamProjectReference(
            abbreviation=project_obj.abbreviation,
            description=project_obj.description,
            id=project_obj.id,
            name=project_obj.name,
            revision=project_obj.revision,
            state=project_obj.state,
            url=project_obj.url,
            visibility=project_obj.visibility)

        build_definition_reference_obj = DefinitionReference(
            created_date=build_definition_obj.created_date,
            project=team_project_reference_obj,
            type=build_definition_obj.type,
            name=build_definition_obj.name,
            id=build_definition_obj.id)

        agent_pool_queue_obj = AgentPoolQueue(
            id=pool_obj.id,
            name=pool_obj.name)

        build_obj = Build(definition=build_definition_reference_obj, queue=agent_pool_queue_obj)

        return self._client.queue_build(build_obj, project_obj.id)


    def create_build_definition(self, build_definition_name, pool_obj,
                                repository_obj, project_obj, repository_branch, repository_type):
        agent_pool_queue_obj = AgentPoolQueue(
            id=pool_obj.id,
            name=pool_obj.name)

        if repository_type == "TfsGit":
            build_repository_obj = BuildRepository(
                default_branch=repository_branch,
                id=repository_obj.id,
                name=repository_obj.name,
                type=repository_type)
        elif repository_type == "GitHub":
            build_repository_obj = BuildRepository(
                default_branch="master",
                id=repository_obj.id,
                properties=repository_obj.properties,
                name=repository_obj.full_name,
                type="GitHub",
                url=repository_obj.properties['cloneUrl'])

        team_project_reference_obj = TeamProjectReference(
            abbreviation=project_obj.abbreviation,
            description=project_obj.description,
            id=project_obj.id,
            name=project_obj.name,
            revision=project_obj.revision,
            state=project_obj.state,
            url=project_obj.url,
            visibility=project_obj.visibility)

        build_definition_obj = BuildDefinition(
            project=team_project_reference_obj,
            type=2,
            name=build_definition_name,
            process=get_build_process(),
            repository=build_repository_obj,
            triggers=get_build_triggers(),
            queue=agent_pool_queue_obj)

        return self._client.create_definition(build_definition_obj, project_obj.id)

    def get_build_definition_by_name(self, definition_name, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        if not definition_name:
            raise ValueError("definition_name")

        definitions = self._client.get_definitions(
            project=project_name,
            name=definition_name)
        return next((d for d in definitions if d.name == definition_name), None)

    def get_build_by_name(self, build_name, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        if not build_name:
            raise ValueError("definition_name")

        builds_unsorted = self._client.get_builds(project=project_name)
        builds = sorted(builds_unsorted, key=lambda x: x.start_time, reverse=True)
        return next((b for b in builds if b.definition.name == build_name), None)

    def get_build_by_id(self, build_id, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        return self._client.get_build(project_name, build_id)

    def get_build_logs(self, build_id, project_name=None):
        if project_name is None:
            project_name = self.project

        if not project_name:
            raise ValueError("project_name")

        return self._client.get_build_logs(project_name, build_id)

    def get_build_log_lines(self, build_id, log_id, start_line=None, end_line=None, project_name=None):
        if project_name is None:
            project_name = self.project

        return self._client.get_build_log_lines(project_name, build_id, log_id, start_line, end_line)

    def get_github_repository_by_name(self, github_service_endpoint, github_repository_name):
        if not self.project:
            raise ValueError("self.project")

        repositories = self._client.list_repositories(
            project=self.project,
            provider_name='github',
            service_endpoint_id=github_service_endpoint.id,
            repository=github_repository_name
        )
        repository_match = next((r for r in repositories.repositories if r.full_name == github_repository_name), None)
        return repository_match

    def get_artifacts(self, build_id):
        if not self.project:
            raise ValueError("self.project")

        return self._client.get_artifacts(self.project, build_id)
