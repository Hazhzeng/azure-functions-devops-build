# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from ..base.base_information import BaseInformation
from ..clients.client_factory import ClientFactory


class ExtensionManager(object):
    """ Manage DevOps Extensions

    Install a new extension within an organization or view existing extensions.
    """

    def __init__(self, organization_name=None, creds=None):
        self._information = BaseInformation(
            credential=creds,
            organization=organization_name)
        self._extension_management = ClientFactory.get_extension_management_client(self._information)

    def create_extension(self, extension_name, publisher_name):
        extensions = self._extension_management.list_extensions()
        extension = next((extension for extension in extensions
                          if (extension.publisher_id == publisher_name)
                          and (extension.extension_id == extension_name)), None)
        # If the extension wasn't in the installed extensions than we know we need to install it
        if extension is None:
            extension = self._extension_management.install_extension(publisher_name, extension_name)

        return extension
