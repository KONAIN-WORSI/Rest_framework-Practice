from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken


class LogoutViewTests(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="logout-user@example.com",
            username="logout-user",
            password="test-password",
        )
        self.refresh = RefreshToken.for_user(self.user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {self.refresh.access_token}"
        )

    def test_logout_blacklists_refresh_token(self):
        response = self.client.post(
            "/api/auth/logout/",
            {"refresh": str(self.refresh)},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)
        self.assertTrue(
            BlacklistedToken.objects.filter(token__jti=self.refresh["jti"]).exists()
        )

    def test_invalid_refresh_token_returns_bad_request(self):
        response = self.client.post(
            "/api/auth/logout/",
            {"refresh": "not-a-valid-refresh-token"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
