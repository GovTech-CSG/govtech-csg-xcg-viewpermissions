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
from django.apps import AppConfig

from .patch.patch import Patcher


class AcasAppConfig(AppConfig):
    default_auto_field = "django.db.models.AutoField"
    name = "govtech_csg_xcg.viewpermissions"

    def ready(self):
        Patcher.do_patch()
