# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import re
from ..base.base_information import BaseInformation
from ..clients.client_factory import ClientFactory
from ..models import ValidateAccountName


class OrganizationManager():

    msa_organization_names = set()

    def __init__(self, creds=None):
        self._information = BaseInformation(
            credential=creds)
        self._user = ClientFactory.get_user_client(self._information)
        self._organization_listing = ClientFactory.get_organization_listing_client(self._information)
        self._organization_creation = ClientFactory.get_organization_creation_client(self._information)

    def validate_organization_name(self, organization_name):
        if organization_name is None:
            return ValidateAccountName(
                valid=False,
                message="The organization_name cannot be None")

        if re.search("[^0-9A-Za-z-]", organization_name):
            return ValidateAccountName(
                valid=False,
                message="""
                The name supplied contains forbidden characters.
                Only alphanumeric characters and dashes are allowed.
                Please try another organization name.""")

        return self.validate_organization_name(organization_name)

    def list_organizations(self):
        """List what organizations this user is part of"""

        organizations_aad = self._organization_listing.list_organizations(self._user.aad_id, msa=False)
        organizations_msa = self._organization_listing.list_organizations(self._user.msa_id, msa=True)

        # Mark aad organizations as force_msa_pass_through = False
        organizations = organizations_aad
        aad_organization_ids = {o.accountId for o in organizations.value}

        # Merge msa organizations
        for msa_org in organizations_msa.value:
            if msa_org.accountId not in aad_organization_ids:
                organizations.value.append(msa_org)
                self.__class__.msa_organization_names.add(msa_org.accountName.lower())

        # Summarize number of organizations
        organizations.count = len(organizations.value)
        return organizations

    def create_organization(self, region_code, organization_name):
        return self._organization_creation.create_organization(
            region_code=region_code,
            msa=False,
            organization_name=organization_name)
