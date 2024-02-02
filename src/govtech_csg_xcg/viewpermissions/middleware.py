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
import re

from django.conf import settings
from django.contrib.auth.mixins import AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.urls import resolve

from govtech_csg_xcg.viewpermissions import logger

IGNORE_PATHS = [
    re.compile(url) for url in getattr(settings, "XCG_PERMISSION_IGNORE_PATHS", [])
]
IGNORE_PATHS.append(re.compile(settings.LOGIN_URL))

IGNORE_VIEW_NAMES = list(getattr(settings, "XCG_PERMISSION_IGNORE_VIEW_NAMES", []))

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object


class ViewPermissionsMiddleware(MiddlewareMixin):
    """Django Middleware to provide permission control for Django Views"""

    # need for one time initialization, here response is a function which will be called to get response from view/template
    def __init__(self, get_response):
        super().__init__(get_response)
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.

        response = self.get_response(request)
        # Code to be executed for each request/response after the view is called.

        return response

    # this is called before requesting response
    def process_view(self, request, view_func, view_args, view_kwargs):
        # If authenticated return no exception

        # Check if func has set the Django built-in authentication or authorization decorators
        if getattr(view_func, "user_passes_test_set", False):
            return

        # Check if class inherits from AccessMixin
        # If it does, it means the class-based view is already enforcing some form of access control
        view_class = getattr(view_func, "view_class", None)
        if view_class and issubclass(view_class, AccessMixin):
            return

        path = request.path

        try:
            resolver = resolve(path)
        except Http404:
            return redirect_to_login(request.get_full_path())

        # For views in VIEW whitelist set in Django settings
        if resolver.view_name in IGNORE_VIEW_NAMES:
            return

        # For URLs in URL whitelist set in Django settings
        if any(url.match(path) for url in IGNORE_PATHS):
            return

        # For the View without the decorator "view_permission" set, return PermissionDenied or turn to the login page
        if request.user.is_authenticated:
            logger.info(
                f"[Middleware] - Blocking user '{request.user.username}' for access the view '{resolver.view_name}'"
            )
            raise PermissionDenied
        else:
            return redirect_to_login(request.get_full_path())
