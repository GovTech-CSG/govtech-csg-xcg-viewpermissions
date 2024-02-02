from django.urls import path

from . import views

urlpatterns = [
    path("private_function_based/", views.private_function_based),
    path("private_class_based/", views.PrivateClassBased.as_view()),
    path(
        "private_whitelisted_function_based/", views.private_whitelisted_function_based
    ),
    path(
        "private_whitelisted_class_based/",
        views.PrivateWhitelistedClassBased.as_view(),
        name="private-whitelisted",
    ),
    path("public_function_based/", views.public_function_based),
    path("public_class_based/", views.PublicClassBased.as_view()),
    path("login_required_function_based/", views.login_required_function_based),
    path("login_required_class_based/", views.LoginRequiredClassBased.as_view()),
    path(
        "login_required_whitelisted_function_based/",
        views.login_required_whitelisted_function_based,
    ),
    path(
        "login_required_whitelisted_class_based/",
        views.LoginRequiredWhitelistedClassBased.as_view(),
        name="login-required-whitelisted",
    ),
    path(
        "permission_required_function_based/", views.permission_required_function_based
    ),
    path(
        "permission_required_class_based/", views.PermissionRequiredClassBased.as_view()
    ),
    path("user_passes_test_function_based/", views.user_passes_test_function_based),
    path("user_passes_test_class_based/", views.UserPassesTestClassBased.as_view()),
]
