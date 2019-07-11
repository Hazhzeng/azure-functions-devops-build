# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import os
import time
from collections import OrderedDict
from ..base.base_information import BaseInformation
from ..clients.client_factory import ClientFactory
from ..exceptions import BuildErrorException


class BuilderManager(object):
    """ Manage DevOps Builds

    This class enables users to create DevOps build definitions and builds specifically for yaml file builds.
    It can also be used to retrieve existing build definitions and builds.
    """

    def __init__(self, organization_name=None, project_name=None, repository_name=None, creds=None):
        self._information = BaseInformation(
            credential=creds,
            organization=organization_name,
            project=project_name,
            repository=repository_name)
        self._core = ClientFactory.get_core_client(self._information)
        self._build = ClientFactory.get_build_client(self._information)
        self._task_agent = ClientFactory.get_task_agent_client(self._information)
        self._service_endpoint = ClientFactory.get_service_endpoint_client(self._information)
        self._git = ClientFactory.get_git_client(self._information)

    def create_devops_build_definition(self, build_definition_name, pool_name):
        """
        :rtype: [azure.devops.v5_1.build.models.BuildDefinition]
        """

        project_obj = self._core.get_project_by_name()
        if not project_obj:
            raise BuildErrorException("project_obj is None")

        pool_obj = self._task_agent.get_agent_pool_by_name(pool_name)
        if not pool_obj:
            raise BuildErrorException("pool_obj is None")

        repository_name = self._information.get_repository()
        repository_obj = self._git.get_repository_by_name(repository_name)
        if not repository_obj:
            raise BuildErrorException("repository_obj is None")

        return self._build.create_definition(
            build_definition_name=build_definition_name,
            pool_obj=pool_obj,
            repository_obj=repository_obj,
            project_obj=project_obj,
            repository_branch="master",
            repository_type="TfsGit")

    def create_github_build_definition(self, build_definition_name, pool_name, github_repository):
        """
        :rtype: [azure.devops.v5_1.build.models.BuildDefinition]
        """

        project_obj = self._core.get_project_by_name()
        if not project_obj:
            raise BuildErrorException("project_obj is None")

        pool_obj = self._task_agent.get_agent_pool_by_name(pool_name)
        if not pool_obj:
            raise BuildErrorException("pool_obj is None")

        github_service_endpoint = self._service_endpoint.get_github_service_endpoints()
        repository_obj = self._build.get_github_repository_by_name(github_service_endpoint, github_repository)
        if not repository_obj:
            raise BuildErrorException("repository_obj is None")

        return self._build.create_definition(
            build_definition_name=build_definition_name,
            pool_obj=pool_obj,
            repository_obj=repository_obj,
            project_obj=project_obj,
            repository_branch="master",
            repository_type="GitHub")

    def create_build(self, build_definition_name, pool_name):
        """
        :rtype: [azure.devops.v5_1.build.models.Build]
        """

        project_obj = self._core.get_project_by_name()
        if not project_obj:
            raise BuildErrorException("project_obj is None")

        pool_obj = self._task_agent.get_agent_pool_by_name(pool_name)
        if not pool_obj:
            raise BuildErrorException("pool_obj is None")

        build_definition_obj = self._build.get_build_definition_by_name(build_definition_name)
        if not build_definition_obj:
            raise BuildErrorException("build_definition_obj is None")

        return self._build.create_build(
            pool_obj=pool_obj,
            project_obj=project_obj,
            build_definition_obj=build_definition_obj)

    def poll_build(self, build_name):
        build = self._build.get_build_by_name(build_name)
        while build.status != 'completed':
            time.sleep(1)
            build = self._build.get_build_by_id(build.id)
        return build

    def get_build_logs_status(self, build_id):
        """
        :rtype: { int: azure.devops.v5_1.build.models.build_log }
        """

        build_logs = self._build.get_build_logs(build_id)
        result = OrderedDict()
        for build_log in build_logs:
            result[build_log.id] = build_log
        return result

    # Return the log content by the difference between two logs
    def get_build_logs_content_from_statuses(self, build_id, prev_logs_status=None, curr_logs_status=None):
        """
        :rtype: [ str ]
        """

        if prev_logs_status is None:
            prev_logs_status = {}

        if curr_logs_status is None:
            curr_logs_status = {}

        result = []
        for log_id in curr_logs_status:
            log_content = self._get_log_content_by_id(
                build_id,
                prev_logs_status.get(log_id),
                curr_logs_status.get(log_id)
            )
            result.extend(log_content)

        return os.linesep.join(result)

    # Return the log content by single build_log
    def _get_log_content_by_id(self, build_id, prev_log_status=None, curr_log_status=None):
        if prev_log_status is None or prev_log_status.line_count is None:
            starting_line = 0
        else:
            starting_line = prev_log_status.line_count

        if curr_log_status is None or curr_log_status.line_count is None:
            ending_line = 0
        else:
            ending_line = curr_log_status.line_count

        if starting_line >= ending_line:
            return []

        return self._build.get_build_log_lines(
            build_id,
            curr_log_status.id,
            starting_line,
            ending_line)
