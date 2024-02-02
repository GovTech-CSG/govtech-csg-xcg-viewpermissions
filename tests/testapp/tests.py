import logging

from django.conf import settings
from django.contrib.auth.models import Permission, User
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from parameterized import parameterized

logging.getLogger("viewpermissions").setLevel(logging.ERROR)


class TestViewPermissions(TestCase):
    """Unit tests for the govtech_csg_xcg.viewpermissions package."""

    @classmethod
    def setUpClass(cls):
        # Create our three types of users
        User.objects.create_user(username="normal_user", password="password")

        normal_user_with_permissions = User.objects.create_user(
            username="normal_user_with_permissions", password="password"
        )
        custom_permission = Permission.objects.create(
            codename="custom_permission",
            name="Custom permission",
            content_type=ContentType.objects.get_for_model(User),
        )
        normal_user_with_permissions.user_permissions.add(custom_permission)

        User.objects.create_user(username="special_user", password="password")

    @classmethod
    def tearDownClass(cls):
        pass

    @parameterized.expand(
        [
            ("/private_function_based/",),
            ("/private_class_based/",),
        ]
    )
    def test_private_view_redirect_unauthenticated_users(self, path):
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.headers["Location"], f"{settings.LOGIN_URL}?next={path}"
        )

    @parameterized.expand(
        [
            ("normal_user", "/private_function_based/"),
            ("normal_user", "/private_class_based/"),
            ("normal_user_with_permissions", "/private_function_based/"),
            ("normal_user_with_permissions", "/private_class_based/"),
            ("special_user", "/private_function_based/"),
            ("special_user", "/private_class_based/"),
        ]
    )
    def test_private_view_returns_403_forbidden_to_authenticated_users(
        self, username, path
    ):
        self.client.login(username=username, password="password")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")

    @parameterized.expand(
        [
            (None, "/private_whitelisted_function_based/"),
            (None, "/private_whitelisted_class_based/"),
            ("normal_user", "/private_whitelisted_function_based/"),
            ("normal_user", "/private_whitelisted_class_based/"),
            ("normal_user_with_permissions", "/private_whitelisted_function_based/"),
            ("normal_user_with_permissions", "/private_whitelisted_class_based/"),
            ("special_user", "/private_whitelisted_function_based/"),
            ("special_user", "/private_whitelisted_class_based/"),
        ]
    )
    def test_whitelisted_private_view_allows_all_users(self, username, path):
        if username:
            self.client.login(username=username, password="password")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            (None, "/public_function_based/"),
            (None, "/public_class_based/"),
            ("normal_user", "/public_function_based/"),
            ("normal_user", "/public_class_based/"),
            ("normal_user_with_permissions", "/public_function_based/"),
            ("normal_user_with_permissions", "/public_class_based/"),
            ("special_user", "/public_function_based/"),
            ("special_user", "/public_class_based/"),
        ]
    )
    def test_public_view_allows_all_users(self, username, path):
        if username:
            self.client.login(username=username, password="password")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    @parameterized.expand(
        [
            ("/login_required_function_based/",),
            ("/login_required_whitelisted_function_based/",),
            ("/login_required_class_based/",),
            ("/login_required_whitelisted_class_based/",),
        ]
    )
    def test_login_required_view_redirects_unauthenticated_users(self, path):
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.headers["Location"], f"{settings.LOGIN_URL}?next={path}"
        )

    @parameterized.expand(
        [
            ("normal_user", "/login_required_function_based/"),
            ("normal_user", "/login_required_class_based/"),
            ("normal_user", "/login_required_whitelisted_function_based/"),
            ("normal_user", "/login_required_whitelisted_class_based/"),
            ("normal_user_with_permissions", "/login_required_function_based/"),
            ("normal_user_with_permissions", "/login_required_class_based/"),
            (
                "normal_user_with_permissions",
                "/login_required_whitelisted_function_based/",
            ),
            (
                "normal_user_with_permissions",
                "/login_required_whitelisted_class_based/",
            ),
            ("special_user", "/login_required_function_based/"),
            ("special_user", "/login_required_class_based/"),
            ("special_user", "/login_required_whitelisted_function_based/"),
            ("special_user", "/login_required_whitelisted_class_based/"),
        ]
    )
    def test_login_required_view_allows_all_authenticated_users(self, username, path):
        self.client.login(username=username, password="password")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    # This is necessary due to some strange discrepancy between the
    # permission_required function decorator and the PermissionRequiredMixin
    # base class from which class-based views inherit. The former's
    # default behaviour is to redirect any permissionless user,
    # authenticated or not, while the latter returns 403 Forbidden.
    @parameterized.expand(
        [
            (
                None,
                "/permission_required_function_based/",
            ),
            (
                "normal_user",
                "/permission_required_function_based/",
            ),
            (
                "special_user",
                "/permission_required_function_based/",
            ),
        ]
    )
    def test_permission_required_function_based_view_redirects_users_with_no_permission(
        self, username, path
    ):
        if username:
            self.client.login(username=username, password="password")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.headers["Location"], f"{settings.LOGIN_URL}?next={path}"
        )

    @parameterized.expand(
        [
            ("normal_user", "/permission_required_class_based/"),
            ("special_user", "/permission_required_class_based/"),
        ]
    )
    def test_permission_required_class_based_view_returns_403_forbidden_to_users_with_no_permission(
        self, username, path
    ):
        if username:
            self.client.login(username=username, password="password")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")

    @parameterized.expand(
        [
            ("normal_user_with_permissions", "/permission_required_function_based/"),
            ("normal_user_with_permissions", "/permission_required_class_based/"),
        ]
    )
    def test_permission_required_view_allows_user_with_permission(self, username, path):
        self.client.login(username=username, password="password")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)

    # This is necessary due to some strange discrepancy between the
    # permission_required function decorator and the PermissionRequiredMixin
    # base class from which class-based views inherit. The former's
    # default behaviour is to redirect any permissionless user,
    # authenticated or not, while the latter returns 403 Forbidden.
    @parameterized.expand(
        [
            (
                None,
                "/user_passes_test_function_based/",
            ),
            (
                "normal_user",
                "/user_passes_test_function_based/",
            ),
            (
                "normal_user_with_permissions",
                "/user_passes_test_function_based/",
            ),
        ]
    )
    def test_user_passes_test_function_based_view_redirects_users_who_fail_test(
        self, username, path
    ):
        if username:
            self.client.login(username=username, password="password")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.headers["Location"], f"{settings.LOGIN_URL}?next={path}"
        )

    @parameterized.expand(
        [
            ("normal_user", "/user_passes_test_class_based/"),
            ("normal_user_with_permissions", "/user_passes_test_class_based/"),
        ]
    )
    def test_user_passes_test_class_based_view_returns_403_forbidden_to_users_who_fail_test(
        self, username, path
    ):
        if username:
            self.client.login(username=username, password="password")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 403)
        self.assertTemplateUsed(response, "403.html")

    @parameterized.expand(
        [
            ("special_user", "/user_passes_test_function_based/"),
            ("special_user", "/user_passes_test_class_based/"),
        ]
    )
    def test_user_passes_test_view_allows_users_who_pass_test(self, username, path):
        self.client.login(username=username, password="password")
        response = self.client.get(path)
        self.assertEqual(response.status_code, 200)
