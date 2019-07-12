# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.devops.v5_1.release.models import (
    Artifact,
    ReleaseDefinitionApprovalStep,
    ReleaseDefinitionApprovals,
    EnvironmentRetentionPolicy)


def blob_task(connected_service_name_arm, storage_name):
    blobtask = {}
    blobtask["name"] = "AzureBlob File Copy"
    blobtask["enabled"] = True
    blobtask_inputs = {}
    blobtask_inputs["SourcePath"] = "$(System.DefaultWorkingDirectory)/drop/drop/build$(Build.BuildId).zip"
    blobtask_inputs["ConnectedServiceNameSelector"] = 'ConnectedServiceNameARM'
    blobtask_inputs["ConnectedServiceNameARM"] = connected_service_name_arm
    blobtask_inputs["Destination"] = "AzureBlob"
    blobtask_inputs["StorageAccountRM"] = storage_name
    blobtask_inputs["ContainerName"] = 'azure-build'
    blobtask_inputs["outputStorageUri"] = "outputstorageuri"
    blobtask_inputs["outputStorageContainerSasToken"] = "sastoken"
    blobtask["inputs"] = blobtask_inputs
    blobtask["version"] = "2.*"
    blobtask["definitionType"] = "task"
    blobtask["taskId"] = "eb72cb01-a7e5-427b-a8a1-1b31ccac8a43"
    return blobtask


def sas_token_task(connected_service_name_arm, storage_name):
    sastokentask = {}
    sastokentask["name"] = "Create SAS Token for Storage Account " + storage_name
    sastokentask["enabled"] = True
    sastokentask["taskId"] = "9e0b2bda-6a8d-4215-8e8c-3d47614db813"
    sastokentask["version"] = "1.*"
    sastokentask["definitionType"] = "task"
    sastokentask_inputs = {}
    sastokentask_inputs["ConnectedServiceName"] = connected_service_name_arm
    sastokentask_inputs["StorageAccountRM"] = storage_name
    sastokentask_inputs["SasTokenTimeOutInHours"] = 10000
    sastokentask_inputs["Permission"] = "r"
    sastokentask_inputs["StorageContainerName"] = "azure-build"
    sastokentask_inputs["outputStorageUri"] = "storageUri"
    sastokentask_inputs["outputStorageContainerSasToken"] = "storageToken"
    sastokentask["inputs"] = sastokentask_inputs
    return sastokentask


def app_settings_task(connected_service_name_arm, functionapp_name, resource_name):
    appsetttingstask = {}
    appsetttingstask["name"] = "Set App Settings: "
    appsetttingstask["enabled"] = True
    appsetttingstask["taskId"] = "9d2e4cf0-f3bb-11e6-978b-770d284f4f2d"
    appsetttingstask["version"] = "2.*"
    appsetttingstask["definitionType"] = "task"
    appsetttingstask_inputs = {}
    appsetttingstask_inputs["ConnectedServiceName"] = connected_service_name_arm
    appsetttingstask_inputs["WebAppName"] = functionapp_name
    appsetttingstask_inputs["ResourceGroupName"] = resource_name
    appsetttingstask_inputs["AppSettings"] = (
        "WEBSITE_RUN_FROM_PACKAGE='$(storageUri)/build$(Build.BuildId).zip$(storageToken)'"
    )
    appsetttingstask["inputs"] = appsetttingstask_inputs
    return appsetttingstask


def app_settings_task_customized(connected_service_name_arm, functionapp_name, resource_name, settings):
    appsetttingstask = {}
    appsetttingstask["name"] = "Set App Settings: "
    appsetttingstask["enabled"] = True
    appsetttingstask["taskId"] = "9d2e4cf0-f3bb-11e6-978b-770d284f4f2d"
    appsetttingstask["version"] = "2.*"
    appsetttingstask["definitionType"] = "task"
    appsetttingstask_inputs = {}
    appsetttingstask_inputs["ConnectedServiceName"] = connected_service_name_arm
    appsetttingstask_inputs["WebAppName"] = functionapp_name
    appsetttingstask_inputs["ResourceGroupName"] = resource_name
    appsetttingstask_inputs["AppSettings"] = settings
    appsetttingstask["inputs"] = appsetttingstask_inputs
    return appsetttingstask


def app_service_deploy_task_linux(connected_service_name_arm, functionapp_name):
    appservicetask = {}
    appservicetask["name"] = "Azure App Service Deploy: " + functionapp_name
    appservicetask["enabled"] = True
    appservicetask["taskId"] = "497d490f-eea7-4f2b-ab94-48d9c1acdcb1"
    appservicetask["version"] = "4.*"
    appservicetask["definitionType"] = "task"
    appservicetask_inputs = {}
    appservicetask_inputs["ConnectionType"] = "AzureRM"
    appservicetask_inputs["ConnectedServiceName"] = connected_service_name_arm
    appservicetask_inputs["PublishProfilePath"] = "$(System.DefaultWorkingDirectory)/**/*.pubxml"
    appservicetask_inputs["WebAppKind"] = "functionAppLinux"
    appservicetask_inputs["WebAppName"] = functionapp_name
    appservicetask_inputs["SlotName"] = "production"
    appservicetask_inputs["Package"] = "$(System.DefaultWorkingDirectory)/**/*.zip"
    appservicetask["inputs"] = appservicetask_inputs
    return appservicetask


def app_service_deploy_task_windows(connected_service_name_arm, functionapp_name):
    appservicetask = {}
    appservicetask["name"] = "Azure App Service Deploy: " + functionapp_name
    appservicetask["enabled"] = True
    appservicetask["taskId"] = "497d490f-eea7-4f2b-ab94-48d9c1acdcb1"
    appservicetask["version"] = "4.*"
    appservicetask["definitionType"] = "task"
    appservicetask_inputs = {}
    appservicetask_inputs["ConnectionType"] = "AzureRM"
    appservicetask_inputs["ConnectedServiceName"] = connected_service_name_arm
    appservicetask_inputs["PublishProfilePath"] = "$(System.DefaultWorkingDirectory)/**/*.pubxml"
    appservicetask_inputs["WebAppKind"] = "functionAppWindows"
    appservicetask_inputs["WebAppName"] = functionapp_name
    appservicetask_inputs["SlotName"] = "production"
    appservicetask_inputs["Package"] = "$(System.DefaultWorkingDirectory)/**/*.zip"
    appservicetask["inputs"] = appservicetask_inputs
    return appservicetask


def get_triggers(artifact_name):
    trigger = {}
    trigger["triggerType"] = "artifactSource"
    trigger["triggerConditions"] = []
    trigger["artifactAlias"] = artifact_name
    triggers = [trigger]
    return triggers


def get_deployment_input(pool_id):
    deployment_input = {}
    deployment_input["parallelExecution"] = {"parallelExecutionType": 0}
    deployment_input["queueId"] = pool_id
    return deployment_input


def get_phase_inputs(artifact_name):
    phase_inputs = {}
    download_input = {}
    download_input["artifactItems"] = []
    download_input["alias"] = artifact_name
    download_input["artifactType"] = "Build"
    download_input["artifactDownloadMode"] = "All"
    artifacts_download_input = {}
    artifacts_download_input["downloadInputs"] = [download_input]
    phase_input_artifact_download_input = {}
    phase_input_artifact_download_input["skipArtifactsDownload"] = False
    phase_input_artifact_download_input["artifactsDownloadInput"] = artifacts_download_input
    phase_inputs["phaseinput_artifactdownloadinput"] = phase_input_artifact_download_input
    return phase_inputs


def get_deploy_phases(deployment_input, workflowtasks, phase_inputs):
    deploy_phase = {}
    deploy_phase["deploymentInput"] = deployment_input
    deploy_phase["rank"] = 1
    deploy_phase["phaseType"] = 1
    deploy_phase["name"] = "Agent Job"
    deploy_phase["workflowTasks"] = workflowtasks
    deploy_phase["phaseInputs"] = phase_inputs
    deploy_phases = [deploy_phase]
    return deploy_phases


def get_artifact_model(build, project, artifact_id, artifact_name):
    definition_reference = {}
    definition_reference["project"] = {"id": project.id, "name": project.name}
    definition_reference["definition"] = {"id": build.definition.id, "name": build.definition.name}
    definition_reference["defaultVersionType"] = {"id": "latestType", "name": "Latest"}

    return Artifact(
        source_id=artifact_id,
        alias=artifact_name,
        type="Build",
        definition_reference=definition_reference)


def get_pre_post_approvals():
    pre_approval = ReleaseDefinitionApprovalStep(
        id=0,
        rank=1,
        is_automated=True,
        is_notification_on=False
    )

    post_approval = ReleaseDefinitionApprovalStep(
        id=0,
        rank=1,
        is_automated=True,
        is_notification_on=False
    )

    pre_release_approvals = ReleaseDefinitionApprovals(
        approvals=[pre_approval]
    )

    post_release_approvals = ReleaseDefinitionApprovals(
        approvals=[post_approval]
    )

    return pre_release_approvals, post_release_approvals


def get_retention_policy():
    return EnvironmentRetentionPolicy(
        days_to_keep=300,
        releases_to_keep=3,
        retain_build=True)
