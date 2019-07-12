# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.devops.v5_1.release.models import (
    ReleaseDefinitionDeployStep,
    ReleaseDefinitionEnvironment,
    ReleaseDefinition,
    Condition)
from ..base.base_information import BaseInformation
from ..clients.client_factory import ClientFactory
from ..constants import (
    LINUX_CONSUMPTION,
    LINUX_DEDICATED,
    WINDOWS)
from ..exceptions import ReleaseErrorException
from ..utils.release_utils import (
    blob_task,
    sas_token_task,
    app_settings_task,
    app_service_deploy_task_linux,
    app_service_deploy_task_windows,
    app_settings_task_customized,
    get_retention_policy,
    get_artifact_model,
    get_pre_post_approvals,
    get_triggers,
    get_deployment_input,
    get_phase_inputs,
    get_deploy_phases)


class ReleaseManager(object):

    def __init__(self, organization_name="", project_name="", creds=None):
        self._information = BaseInformation(
            credential=creds,
            organization=organization_name,
            project=project_name)
        self._core = ClientFactory.get_core_client(self._information)
        self._devops_rest = ClientFactory.get_devops_rest_client(self._information)
        self._build = ClientFactory.get_build_client(self._information)
        self._release = ClientFactory.get_release_client(self._information)
        self._service_endpoint = ClientFactory.get_service_endpoint_client(self._information)

    def create_release_definition(self, build_name, artifact_name, pool_name, service_endpoint_name,
                                  release_definition_name, app_type, functionapp_name, storage_name,
                                  resource_name, settings=None):
        pool = self._devops_rest.get_pool_by_name(False, pool_name)
        project = self._core.get_project_by_name()
        build = self._build.get_build_by_name(build_name)
        retention_policy_environment = get_retention_policy()

        artifact = self._build.get_artifact_by_name(build.id, artifact_name)
        artifact_obj = get_artifact_model(build, project, artifact.id, artifact.name)

        pre_release_approvals, post_release_approvals = get_pre_post_approvals()
        service_endpoint = self._service_endpoint.get_service_endpoints_by_name(service_endpoint_name)
        triggers = get_triggers(artifact_name)
        deployment_input = get_deployment_input(pool.id)

        phase_inputs = get_phase_inputs(artifact_name)

        workflowtasks = []

        if app_type == LINUX_CONSUMPTION:
            workflowtasks.append(blob_task(service_endpoint.id, storage_name))
            workflowtasks.append(sas_token_task(service_endpoint.id, storage_name))
            workflowtasks.append(app_settings_task(service_endpoint.id, functionapp_name, resource_name))
        elif app_type == LINUX_DEDICATED:
            workflowtasks.append(app_service_deploy_task_linux(service_endpoint.id, functionapp_name))
        elif app_type == WINDOWS:
            workflowtasks.append(app_service_deploy_task_windows(service_endpoint.id, functionapp_name))
        else:
            raise ReleaseErrorException("Invalid app type provided. Accepts: {} {} {}".format(
                LINUX_CONSUMPTION, LINUX_DEDICATED, WINDOWS))

        if settings is not None:
            settings_str = ""
            for setting in settings:
                settings_str += (setting[0] + "='" + setting[1] + "'")
            # Check that settings were actually set otherwise we don't want to use the task
            if settings_str != "":
                workflowtasks.append(app_settings_task_customized(
                    service_endpoint.id, functionapp_name, resource_name, settings_str
                ))

        deploy_phases = get_deploy_phases(deployment_input, workflowtasks, phase_inputs)

        release_deploy_step = ReleaseDefinitionDeployStep(id=2)

        condition = Condition(condition_type=1, name="ReleaseStarted", value="")

        release_definition_environment = ReleaseDefinitionEnvironment(
            name="deploy build",
            rank=1,
            retention_policy=retention_policy_environment,
            pre_deploy_approvals=pre_release_approvals,
            post_deploy_approvals=post_release_approvals,
            deploy_phases=deploy_phases,
            deploy_step=release_deploy_step,
            conditions=[condition]
        )

        release_definition = ReleaseDefinition(
            name=release_definition_name,
            environments=[release_definition_environment],
            artifacts=[artifact_obj],
            triggers=triggers
        )

        return self._release.create_release_definition(release_definition)

    def create_release(self, release_definition_name):
        release_definition = self._release.get_release_definition_by_name(release_definition_name)
        return self._release.create_release(release_definition.id)

    def list_release_definitions(self):
        return self._release.get_release_definitions()

    def list_releases(self):
        return self._release.get_releases()

    def get_latest_release(self, release_definition_name):
        build_definition = self._release.get_release_definition_by_name(release_definition_name)
        releases = self._release.get_releases_by_definition_id(build_definition.id)
        releases.sort(key=lambda r: r.id, reverse=True)
        return releases[0] if releases else None
