import uuid

from django.contrib.auth.models import AnonymousUser, Group, User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APIRequestFactory, APITestCase

from main.models import Education, Project
from main.serializers import EducationSerializer


class ProjectAPITest(APITestCase):
    def setUp(self):
        self.owner = User.objects.create_superuser(
            username="owner", password="test-password", email="owner@example.com",
        )
        self.visitor = User.objects.create_user(username="visitor", password="test-password")
        self.project = Project.objects.create(
            title="Portfolio", description="My website", tech_stack="Django",
        )
        self.list_url = reverse("api:project-list")
        self.detail_url = reverse("api:project-detail", args=[self.project.id])
        self.star_url = reverse("api:project-star", args=[self.project.id])
        self.payload = {
            "title": "New project", "description": "A useful app", "tech_stack": "Python",
            "project_url": "https://example.com/", "project_image_url": "",
        }

    def test_public_list_and_detail(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], str(self.project.id))
        self.assertFalse(response.data[0]["is_starred"])
        self.assertNotIn("fields", response.data[0])
        self.assertEqual(self.client.get(self.detail_url).status_code, status.HTTP_200_OK)

    def test_search_and_empty_results(self):
        response = self.client.get(self.list_url, {"title": "PORT"})
        self.assertEqual(len(response.data), 1)
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.data, [])

    def test_missing_project(self):
        url = reverse("api:project-detail", args=[uuid.uuid4()])
        self.assertEqual(self.client.get(url).status_code, status.HTTP_404_NOT_FOUND)

    def test_guest_and_visitor_cannot_write(self):
        for user in (None, self.visitor):
            self.client.force_authenticate(user=user)
            self.assertEqual(self.client.post(self.list_url, self.payload, format="json").status_code, 403)
            self.assertEqual(self.client.patch(self.detail_url, {"title": "Changed"}, format="json").status_code, 403)
            self.assertEqual(self.client.delete(self.detail_url).status_code, 403)
        self.assertEqual(Project.objects.count(), 1)
        self.project.refresh_from_db()
        self.assertEqual(self.project.title, "Portfolio")

    def test_owner_can_create(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.filter(pk=response.data["id"]).exists())

    def test_validation(self):
        self.client.force_authenticate(user=self.owner)
        for changes, field in [
            ({"title": "   "}, "title"),
            ({"title": '<img src="x" onerror="alert(1)">'}, "title"),
            ({"project_url": "javascript:alert(1)"}, "project_url"),
        ]:
            response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertIn(field, response.data)
        self.assertEqual(Project.objects.count(), 1)

    def test_patch_put_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.project.refresh_from_db()
        self.assertEqual(self.project.description, "My website")
        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Project.objects.filter(pk=self.project.id).exists())

    def test_star_requires_login_and_toggles(self):
        self.assertEqual(self.client.post(self.star_url).status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.visitor)
        response = self.client.post(self.star_url)
        self.assertTrue(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        response = self.client.post(self.star_url)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 0)

    def test_computed_fields_are_read_only(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, {
            **self.payload, "star_count": 99, "is_starred": True,
            "starred_by_names": "forged", "starred_by": [self.visitor.id],
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

    def test_staff_and_editor_cannot_manage_tutorial_projects(self):
        self.visitor.is_staff = True
        self.visitor.save()
        self.visitor.groups.add(Group.objects.create(name="Editor"))
        self.client.force_authenticate(user=self.visitor)
        response = self.client.patch(self.detail_url, {"title": "Changed"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_wrong_method(self):
        self.client.force_authenticate(user=self.owner)
        self.assertEqual(self.client.delete(self.list_url).status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_session_write_without_csrf_is_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="owner", password="test-password"))
        response = client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Project.objects.count(), 1)

    def test_session_write_with_csrf_succeeds(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username="owner", password="test-password")
        # The Browsable API form renders a real CSRF token into the response.
        page = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(page.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class EducationAPITest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.owner = User.objects.create_superuser(
            username="education-owner", password="test-password", email="owner@example.com",
        )
        cls.regular = User.objects.create_user(
            username="education-user", password="test-password",
        )
        cls.editor = User.objects.create_user(
            username="education-editor", password="test-password",
        )
        cls.editor.groups.add(Group.objects.create(name="Editor"))
        cls.education = Education.objects.create(
            title="S1 Sistem Informasi", institution="Universitas Indonesia",
            major="Sistem Informasi", description="Belajar pengembangan aplikasi.",
            start_year=2025, end_year=2029,
        )

    def setUp(self):
        self.list_url = reverse("api:education-list")
        self.detail_url = reverse("api:education-detail", args=[self.education.pk])
        self.star_url = reverse("api:education-star", args=[self.education.pk])
        self.payload = {
            "title": "S2 Sistem Informasi", "institution": "Universitas Indonesia",
            "major": "Sistem Informasi", "description": "Pendidikan lanjutan.",
            "thumbnail": "https://example.com/logo.png",
            "start_year": 2030, "end_year": None,
        }

    def test_all_roles_can_read_list_and_detail(self):
        self.assertEqual(self.list_url, "/api/v1/education/")
        for user in (None, self.regular, self.editor, self.owner):
            self.client.force_authenticate(user=user)
            with self.subTest(user=user):
                response = self.client.get(self.list_url)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data[0]["id"], str(self.education.pk))
                self.assertNotIn("fields", response.data[0])
                response = self.client.get(self.detail_url)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertEqual(response.data["title"], self.education.title)

    def test_search_is_case_insensitive_and_empty_results_are_a_list(self):
        response = self.client.get(self.list_url, {"title": "  sIsTeM  "})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual([item["id"] for item in response.data], [str(self.education.pk)])
        response = self.client.get(self.list_url, {"title": "not-found"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])

    def test_list_keeps_ongoing_education_first_then_latest_start_year(self):
        ongoing = Education.objects.create(**{**self.payload, "start_year": 2024})
        recent = Education.objects.create(**{**self.payload, "start_year": 2026})
        older = Education.objects.create(**{
            **self.payload, "start_year": 2016, "end_year": 2020,
        })
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [item["id"] for item in response.data],
            [str(item.pk) for item in (recent, ongoing, self.education, older)],
        )

    def test_guest_and_regular_user_cannot_modify_education(self):
        self.education.starred_by.add(self.regular)
        before = self._education_state()
        for user in (None, self.regular):
            self.client.force_authenticate(user=user)
            for method, url, payload in (
                ("post", self.list_url, self.payload),
                ("put", self.detail_url, self.payload),
                ("patch", self.detail_url, {"title": "Unauthorized"}),
                ("delete", self.detail_url, {}),
            ):
                with self.subTest(user=user, method=method):
                    response = getattr(self.client, method)(url, payload, format="json")
                    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                    self.assertEqual(self._education_state(), before)

    def test_editor_can_patch_and_put_but_cannot_create_or_delete(self):
        self.client.force_authenticate(user=self.editor)
        self.education.starred_by.add(self.regular)
        before = self._education_state()
        for method, url, payload in (
            ("post", self.list_url, self.payload),
            ("delete", self.detail_url, {}),
        ):
            response = getattr(self.client, method)(url, payload, format="json")
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.assertEqual(self._education_state(), before)

        response = self.client.patch(self.detail_url, {"title": "<b>Updated</b>"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.title, "Updated")
        self.assertEqual(self.education.description, "Belajar pengembangan aplikasi.")

        response = self.client.put(self.detail_url, {"title": "Incomplete"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.education.refresh_from_db()
        self.assertEqual(self.education.title, "Updated")

        response = self.client.put(self.detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.title, self.payload["title"])
        self.assertEqual(self.education.start_year, 2030)
        self.assertIsNone(self.education.end_year)
        self.assertEqual(list(self.education.starred_by.all()), [self.regular])

    def test_owner_can_create_update_and_delete(self):
        self.client.force_authenticate(user=self.owner)
        response = self.client.post(self.list_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        education = Education.objects.get(pk=response.data["id"])
        self.assertEqual(education.title, self.payload["title"])
        detail_url = reverse("api:education-detail", args=[education.pk])

        response = self.client.patch(detail_url, {"title": "Owner edit"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        education.refresh_from_db()
        self.assertEqual(education.title, "Owner edit")
        response = self.client.put(detail_url, self.payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        education.refresh_from_db()
        self.assertEqual(education.title, self.payload["title"])

        response = self.client.delete(detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Education.objects.filter(pk=education.pk).exists())
        self.assertTrue(Education.objects.filter(pk=self.education.pk).exists())

    def test_invalid_creation_returns_field_errors_without_saving(self):
        self.client.force_authenticate(user=self.owner)
        self.education.starred_by.add(self.regular)
        before = self._education_state()
        for changes, field in (
            ({"title": "<b></b>"}, "title"),
            ({"institution": "   "}, "institution"),
            ({"thumbnail": "javascript:alert(1)"}, "thumbnail"),
            ({"end_year": 2020}, "end_year"),
        ):
            with self.subTest(field=field):
                response = self.client.post(self.list_url, {**self.payload, **changes}, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn(field, response.data)
                self.assertEqual(self._education_state(), before)

    def test_invalid_partial_year_updates_do_not_change_database(self):
        self.client.force_authenticate(user=self.editor)
        self.education.starred_by.add(self.regular)
        before = self._education_state()
        for payload in ({"start_year": 2030}, {"end_year": 2024}):
            with self.subTest(payload=payload):
                response = self.client.patch(self.detail_url, payload, format="json")
                self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
                self.assertIn("end_year", response.data)
                self.assertEqual(self._education_state(), before)

    def test_missing_education_returns_404(self):
        self.client.force_authenticate(user=self.owner)
        self.education.starred_by.add(self.regular)
        before = self._education_state()
        missing_id = uuid.uuid4()
        detail_url = reverse("api:education-detail", args=[missing_id])
        star_url = reverse("api:education-star", args=[missing_id])
        for method, url, payload in (
            ("get", detail_url, {}), ("put", detail_url, self.payload),
            ("patch", detail_url, {"title": "Missing"}),
            ("delete", detail_url, {}), ("post", star_url, {}),
        ):
            with self.subTest(method=method, url=url):
                response = getattr(self.client, method)(url, payload, format="json")
                self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
                self.assertEqual(self._education_state(), before)

    def test_guest_star_is_rejected_without_changing_relation(self):
        self.education.starred_by.add(self.owner)
        before = self._education_state()
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self._education_state(), before)

    def test_authenticated_roles_can_toggle_only_their_own_star(self):
        for user in (self.regular, self.editor, self.owner):
            self.client.force_authenticate(user=user)
            with self.subTest(user=user):
                response = self.client.post(self.star_url, {
                    "user": self.owner.pk, "starred_by": [self.owner.pk],
                }, format="json")
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertTrue(response.data["is_starred"])
                self.assertEqual(response.data["star_count"], 1)
                self.assertEqual(list(self.education.starred_by.all()), [user])
                for url in (self.list_url, self.detail_url):
                    data = self.client.get(url).data
                    item = data[0] if isinstance(data, list) else data
                    self.assertTrue(item["is_starred"])
                    self.assertEqual(item["star_count"], 1)
                response = self.client.post(self.star_url)
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.assertFalse(response.data["is_starred"])
                self.assertEqual(response.data["star_count"], 0)
                self.assertEqual(self.education.starred_by.count(), 0)

    def test_wrong_methods_are_rejected(self):
        self.client.force_authenticate(user=self.owner)
        for method, url in (
            ("delete", self.list_url), ("patch", self.list_url),
            ("post", self.detail_url), ("get", self.star_url),
        ):
            with self.subTest(method=method, url=url):
                self.assertEqual(
                    getattr(self.client, method)(url).status_code,
                    status.HTTP_405_METHOD_NOT_ALLOWED,
                )
        self.assertEqual(Education.objects.count(), 1)
        self.assertEqual(self.education.starred_by.count(), 0)

    def test_session_writes_without_csrf_are_rejected(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="education-owner", password="test-password"))
        self.education.starred_by.add(self.editor)
        before = self._education_state()
        for method, url, payload in (
            ("post", self.list_url, self.payload),
            ("put", self.detail_url, self.payload),
            ("patch", self.detail_url, {"title": "Without CSRF"}),
            ("delete", self.detail_url, {}), ("post", self.star_url, {}),
        ):
            with self.subTest(method=method, url=url):
                response = getattr(client, method)(url, payload, format="json")
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                self.assertIn("CSRF", str(response.data["detail"]))
                self.assertEqual(self._education_state(), before)
        client.logout()
        self.assertTrue(client.login(username="education-user", password="test-password"))
        response = client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("CSRF", str(response.data["detail"]))
        self.assertEqual(self._education_state(), before)

    def test_browsable_api_and_session_writes_with_csrf(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="education-owner", password="test-password"))
        for url in (self.list_url, self.detail_url):
            response = client.get(url, HTTP_ACCEPT="text/html")
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertTrue(response["Content-Type"].startswith("text/html"))
        token = client.cookies["csrftoken"].value
        response = client.post(
            self.list_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        education = Education.objects.get(pk=response.data["id"])
        self.assertEqual(education.title, self.payload["title"])
        detail_url = reverse("api:education-detail", args=[education.pk])
        response = client.patch(
            detail_url, {"title": "With CSRF"}, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        education.refresh_from_db()
        self.assertEqual(education.title, "With CSRF")
        response = client.put(
            detail_url, self.payload, format="json", HTTP_X_CSRFTOKEN=token,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        education.refresh_from_db()
        self.assertEqual(education.title, self.payload["title"])
        response = client.post(self.star_url, HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(self.education.starred_by.filter(pk=self.owner.pk).exists())
        response = client.delete(detail_url, HTTP_X_CSRFTOKEN=token)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.content, b"")
        self.assertFalse(Education.objects.filter(pk=education.pk).exists())

    def test_staff_without_editor_group_cannot_modify_education(self):
        self.regular.is_staff = True
        self.regular.save(update_fields=["is_staff"])
        self.client.force_authenticate(user=self.regular)
        self.education.starred_by.add(self.regular)
        before = self._education_state()
        for method, url, payload in (
            ("post", self.list_url, self.payload),
            ("put", self.detail_url, self.payload),
            ("patch", self.detail_url, {"title": "Staff edit"}),
            ("delete", self.detail_url, {}),
        ):
            with self.subTest(method=method):
                response = getattr(self.client, method)(url, payload, format="json")
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                self.assertEqual(self._education_state(), before)

    def test_star_state_is_personal_and_unstar_preserves_other_users(self):
        self.education.starred_by.add(self.regular)
        self.client.force_authenticate(user=self.editor)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["star_count"], 2)
        for user, expected in (
            (None, False), (self.regular, True), (self.editor, True), (self.owner, False),
        ):
            self.client.force_authenticate(user=user)
            for url in (self.list_url, self.detail_url):
                with self.subTest(user=user, url=url):
                    response = self.client.get(url)
                    self.assertEqual(response.status_code, status.HTTP_200_OK)
                    item = response.data[0] if url == self.list_url else response.data
                    self.assertEqual(item["is_starred"], expected)
                    self.assertEqual(item["star_count"], 2)
                    for field in ("starred_by", "starred_by_names", "email", "password"):
                        self.assertNotIn(field, item)
        self.client.force_authenticate(user=self.editor)
        response = self.client.post(self.star_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data["is_starred"])
        self.assertEqual(response.data["star_count"], 1)
        self.assertEqual(list(self.education.starred_by.all()), [self.regular])

    def test_api_write_payload_cannot_override_star_fields_or_user_relations(self):
        self.client.force_authenticate(user=self.owner)
        forged = {
            "star_count": 99, "is_starred": True, "starred_by": [self.owner.pk],
        }
        response = self.client.post(self.list_url, {**self.payload, **forged}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        education = Education.objects.get(pk=response.data["id"])
        self.assertEqual(education.starred_by.count(), 0)
        self.assertEqual(response.data["star_count"], 0)
        self.assertFalse(response.data["is_starred"])

        self.education.starred_by.add(self.regular)
        response = self.client.patch(self.detail_url, {
            **forged, "title": "Updated without changing stars",
        }, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.education.refresh_from_db()
        self.assertEqual(self.education.title, "Updated without changing stars")
        self.assertEqual(list(self.education.starred_by.all()), [self.regular])
        self.assertEqual(response.data["star_count"], 1)
        self.assertFalse(response.data["is_starred"])

    def test_editor_session_with_csrf_can_edit_but_cannot_create_or_delete(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="education-editor", password="test-password"))
        response = client.get(self.detail_url, HTTP_ACCEPT="text/html")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        for method, payload in (
            ("put", self.payload), ("patch", {"title": "Editor session edit"}),
        ):
            with self.subTest(method=method):
                response = getattr(client, method)(
                    self.detail_url, payload, format="json", HTTP_X_CSRFTOKEN=token,
                )
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                self.education.refresh_from_db()
                self.assertEqual(self.education.title, payload["title"])
        before = self._education_state()
        for method, url, payload in (
            ("post", self.list_url, self.payload), ("delete", self.detail_url, {}),
        ):
            with self.subTest(method=method):
                response = getattr(client, method)(
                    url, payload, format="json", HTTP_X_CSRFTOKEN=token,
                )
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                self.assertNotIn("CSRF", str(response.data["detail"]))
                self.assertEqual(self._education_state(), before)

    def test_regular_session_with_csrf_can_star_but_cannot_modify_education(self):
        client = APIClient(enforce_csrf_checks=True)
        self.assertTrue(client.login(username="education-user", password="test-password"))
        response = client.get(self.list_url, HTTP_ACCEPT="text/html")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = client.cookies["csrftoken"].value
        for expected in (True, False):
            response = client.post(self.star_url, HTTP_X_CSRFTOKEN=token)
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data["is_starred"], expected)
            self.assertEqual(self.education.starred_by.filter(pk=self.regular.pk).exists(), expected)
        before = self._education_state()
        for method, url, payload in (
            ("post", self.list_url, self.payload),
            ("put", self.detail_url, self.payload),
            ("patch", self.detail_url, {"title": "Regular session edit"}),
            ("delete", self.detail_url, {}),
        ):
            with self.subTest(method=method):
                response = getattr(client, method)(
                    url, payload, format="json", HTTP_X_CSRFTOKEN=token,
                )
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
                self.assertNotIn("CSRF", str(response.data["detail"]))
                self.assertEqual(self._education_state(), before)

    def _education_state(self):
        # Include the join table so rejected requests cannot silently change stars.
        return (
            list(Education.objects.order_by("id").values()),
            list(Education.starred_by.through.objects.order_by(
                "education_id", "user_id",
            ).values_list("education_id", "user_id")),
        )


class EducationSerializerTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username="education-reader", email="reader@example.com",
        )
        cls.education = Education.objects.create(
            title="S1 Sistem Informasi", institution="Universitas Indonesia",
            major="Sistem Informasi", description="Belajar pengembangan aplikasi.",
            start_year=2025, end_year=2029,
        )

    def setUp(self):
        self.payload = {
            "title": "S1 Sistem Informasi", "institution": "Universitas Indonesia",
            "major": "Sistem Informasi", "description": "Belajar pengembangan aplikasi.",
            "thumbnail": "https://example.com/logo.png",
            "start_year": 2025, "end_year": 2029,
        }

    def test_text_is_cleaned_before_saving(self):
        fields = ("title", "institution", "major", "description")
        payload = {
            **self.payload,
            **{field: f"  <b>{self.payload[field]}</b>  " for field in fields},
        }
        serializer = EducationSerializer(data=payload)
        self.assertTrue(serializer.is_valid(), serializer.errors)
        education = serializer.save()
        education.refresh_from_db()
        for field in fields:
            self.assertEqual(getattr(education, field), self.payload[field])

    def test_required_text_rejects_blank_and_html_only_values(self):
        for field in ("title", "institution", "major", "description"):
            for value in ("   ", '<img src="x" onerror="alert(1)">'):
                with self.subTest(field=field, value=value):
                    serializer = EducationSerializer(data={**self.payload, field: value})
                    self.assertFalse(serializer.is_valid())
                    self.assertIn(field, serializer.errors)
        self.assertEqual(Education.objects.count(), 1)

    def test_thumbnail_rejects_invalid_or_non_web_urls(self):
        for value in ("not-a-url", "javascript:alert(1)", "ftp://example.com/logo.png"):
            with self.subTest(value=value):
                serializer = EducationSerializer(data={**self.payload, "thumbnail": value})
                self.assertFalse(serializer.is_valid())
                self.assertIn("thumbnail", serializer.errors)

    def test_thumbnail_accepts_web_urls_and_optional_values(self):
        for value in ("https://example.com/logo.png", "http://example.com/logo.png", "", None):
            with self.subTest(value=value):
                serializer = EducationSerializer(data={**self.payload, "thumbnail": value})
                self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_year_range_validation(self):
        serializer = EducationSerializer(data={**self.payload, "end_year": 2024})
        self.assertFalse(serializer.is_valid())
        self.assertIn("end_year", serializer.errors)
        for end_year in (2025, 2029, None):
            with self.subTest(end_year=end_year):
                serializer = EducationSerializer(data={**self.payload, "end_year": end_year})
                self.assertTrue(serializer.is_valid(), serializer.errors)

    def test_partial_update_checks_saved_years(self):
        for data in ({"start_year": 2030}, {"end_year": 2024}):
            with self.subTest(data=data):
                serializer = EducationSerializer(self.education, data=data, partial=True)
                self.assertFalse(serializer.is_valid())
                self.assertIn("end_year", serializer.errors)
                self.education.refresh_from_db()
                self.assertEqual(self.education.start_year, 2025)
                self.assertEqual(self.education.end_year, 2029)

    def test_partial_update_preserves_omitted_fields_and_can_clear_end_year(self):
        serializer = EducationSerializer(
            self.education, data={"title": "<b>Judul baru</b>"}, partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        self.education.refresh_from_db()
        self.assertEqual(self.education.title, "Judul baru")
        self.assertEqual(self.education.start_year, 2025)
        self.assertEqual(self.education.end_year, 2029)

        serializer = EducationSerializer(
            self.education, data={"start_year": 2030, "end_year": None}, partial=True,
        )
        self.assertTrue(serializer.is_valid(), serializer.errors)
        serializer.save()
        self.education.refresh_from_db()
        self.assertEqual(self.education.start_year, 2030)
        self.assertIsNone(self.education.end_year)

    def test_star_information_uses_request_user_without_exposing_accounts(self):
        self.education.starred_by.add(self.user)
        for user, expected in ((AnonymousUser(), False), (self.user, True)):
            with self.subTest(user=user):
                request = APIRequestFactory().get("/")
                request.user = user
                data = EducationSerializer(
                    self.education, context={"request": request},
                ).data
                self.assertEqual(data["star_count"], 1)
                self.assertEqual(data["is_starred"], expected)
                self.assertEqual(set(data), {
                    "id", "title", "institution", "major", "description", "thumbnail",
                    "start_year", "end_year", "created_at", "updated_at",
                    "star_count", "is_starred",
                })
        self.assertFalse(EducationSerializer(self.education).data["is_starred"])

    def test_generated_fields_and_star_relation_cannot_be_overwritten(self):
        forged_id = uuid.uuid4()
        serializer = EducationSerializer(data={
            **self.payload, "id": str(forged_id),
            "created_at": "2000-01-01T00:00:00Z", "updated_at": "2000-01-01T00:00:00Z",
            "star_count": 99, "is_starred": True, "starred_by": [self.user.pk],
        })
        self.assertTrue(serializer.is_valid(), serializer.errors)
        education = serializer.save()
        education.refresh_from_db()
        self.assertNotEqual(education.pk, forged_id)
        self.assertNotEqual(education.created_at.year, 2000)
        self.assertNotEqual(education.updated_at.year, 2000)
        self.assertEqual(education.starred_by.count(), 0)
        self.assertEqual(serializer.data["star_count"], 0)
        self.assertFalse(serializer.data["is_starred"])
