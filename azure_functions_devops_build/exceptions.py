# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------


class CliBaseException(Exception):
    def __init__(self, message=None):
        super().__init__()
        self.message = message


class GitOperationException(CliBaseException):
    pass


class RoleAssignmentException(CliBaseException):
    pass


class LanguageNotSupportException(CliBaseException):
    pass


class BuildErrorException(CliBaseException):
    pass


class ReleaseErrorException(CliBaseException):
    pass


class GithubContentNotFound(CliBaseException):
    pass


class GithubIntegrationRequestError(CliBaseException):
    pass


class GithubUnauthorizedError(CliBaseException):
    pass


class NoConnectionCredentialError(CliBaseException):
    pass


class NoConnectionOrganzationError(CliBaseException):
    pass
