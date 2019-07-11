# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

def get_build_process():
    process = {}
    process["yamlFilename"] = "azure-pipelines.yml"
    process["type"] = 2
    process["resources"] = {}
    return process

def get_build_triggers():
    trigger = {}
    trigger["branchFilters"] = []
    trigger["pathFilters"] = []
    trigger["settingsSourceType"] = 2
    trigger["batchChanges"] = False
    trigger["maxConcurrentBuildsPerBranch"] = 1
    trigger["triggerType"] = "continuousIntegration"
    triggers = [trigger]
    return triggers


