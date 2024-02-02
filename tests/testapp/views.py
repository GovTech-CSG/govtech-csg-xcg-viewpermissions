from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
)
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View

from govtech_csg_xcg.viewpermissions.decorators import public

SUCCESS_RESPONSE = HttpResponse("Successful")


# No decorator FBV
def private_function_based(request):
    return SUCCESS_RESPONSE


# No decorator CBV
class PrivateClassBased(View):
    def get(self, request):
        return SUCCESS_RESPONSE


# No decorator whitelisted FBV
def private_whitelisted_function_based(request):
    return SUCCESS_RESPONSE


# No decorator whitelisted CBV
class PrivateWhitelistedClassBased(View):
    def get(self, request):
        return SUCCESS_RESPONSE


# Public decorator FBV
@public
def public_function_based(request):
    return SUCCESS_RESPONSE


# Public decorator CBV
@method_decorator(public, name="dispatch")
class PublicClassBased(View):
    def get(self, request):
        return SUCCESS_RESPONSE


# Login required FBV
@login_required
def login_required_function_based(request):
    return SUCCESS_RESPONSE


# Login required CBV
class LoginRequiredClassBased(LoginRequiredMixin, View):
    def get(self, request):
        return SUCCESS_RESPONSE


# Login required whitelisted FBV
@login_required
def login_required_whitelisted_function_based(request):
    return SUCCESS_RESPONSE


# Login required whitelisted CBV
class LoginRequiredWhitelistedClassBased(LoginRequiredMixin, View):
    def get(self, request):
        return SUCCESS_RESPONSE


# Permission required FBV
@permission_required("auth.custom_permission")
def permission_required_function_based(request):
    return SUCCESS_RESPONSE


# Permission required CBV
class PermissionRequiredClassBased(PermissionRequiredMixin, View):
    permission_required = "auth.custom_permission"

    def get(self, request):
        return SUCCESS_RESPONSE


# Custom FBV
@user_passes_test(lambda user: user.username == "special_user")
def user_passes_test_function_based(request):
    return SUCCESS_RESPONSE


# Custom CBV
class UserPassesTestClassBased(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.username == "special_user"

    def get(self, request):
        return SUCCESS_RESPONSE
