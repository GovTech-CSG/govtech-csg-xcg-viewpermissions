# ------------------------------------------------------------------------
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
#
# This file incorporates work covered by the following copyright:
#
# Copyright (c) 2024 Agency for Science, Technology and Research (A*STAR).
#   All rights reserved.
# Copyright (c) 2024 Government Technology Agency (GovTech).
#   All rights reserved.
# ------------------------------------------------------------------------
import django

from govtech_csg_xcg.viewpermissions import logger

from .permission import (
    patched_login_required,
    patched_permission_required,
    patched_user_passes_test,
)


class Patcher:
    """this class will do the patching and reverting of Django's built-in view permissions functions"""

    @classmethod
    def do_patch(cls):
        """this function will monkey patch Django's built-in view permissions functions"""
        django.contrib.auth.decorators.user_passes_test = patched_user_passes_test
        django.contrib.auth.decorators.permission_required = patched_permission_required
        django.contrib.auth.decorators.login_required = patched_login_required
        logger.debug("[Patch] - Complete the patch permission functions")

    @classmethod
    def revert(cls):
        """this function will rever back the original functions"""
        django.contrib.auth.decorators.user_passes_test = (
            django.contrib.auth.decorators.orig_user_passes_test_
        )
        django.contrib.auth.decorators.permission_required = (
            django.contrib.auth.decorators.orig_permission_required_
        )
        django.contrib.auth.decorators.login_required = (
            django.contrib.auth.decorators.orig_login_required_
        )
