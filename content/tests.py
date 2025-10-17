from django.test import TestCase
from django.urls import reverse


class HomePageTests(TestCase):
    def test_homepage_renders(self):
        url = reverse("home")
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, "Direkteinstieg")
