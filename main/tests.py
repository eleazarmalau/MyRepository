from django.test import TestCase, Client
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import Group, User

from main.models import Education, Experience

class MainTest(TestCase):
    def setUp(self):
        self.experience = Experience.objects.create(
            title="PBP Teaching Assistant",
            place="Faculty of Computer Science, University of Indonesia",
            description="Help students understand web development.",
            category="part-time",
        )

    def test_main_url_is_accessible(self):
        response = self.client.get(reverse("main:show_main"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertNotContains(response, self.experience.title)
        self.assertContains(response, f'href="{reverse("main:show_experience")}"')

    def test_nonexistent_page_returns_404(self):
        response = self.client.get("/a-page-that-does-not-exist/")

        self.assertEqual(response.status_code, 404)

    def test_experience_model(self):
        self.assertEqual(str(self.experience), "PBP Teaching Assistant")
        self.assertEqual(self.experience.category, "part-time")
        self.assertTrue(self.experience.is_ongoing)

    def test_experience_page(self):
        response = self.client.get(reverse("main:show_experience"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "experience.html")
        self.assertContains(response, self.experience.title)
        self.assertContains(response, self.experience.description)
        self.assertContains(response, "Part-Time")
        self.assertContains(response, "Ongoing")
        self.assertContains(response, f'href="{reverse("main:show_main")}"')

    def test_empty_experience_page(self):
        Experience.objects.all().delete()
        response = self.client.get(reverse("main:show_experience"))

        self.assertContains(response, "No experience has been added yet.")

    def test_completed_experience(self):
        self.experience.ended_at = timezone.now()
        self.experience.save()
        response = self.client.get(reverse("main:show_experience"))

        self.assertFalse(self.experience.is_ongoing)
        self.assertContains(response, "Completed")
        self.assertNotContains(response, "Ongoing")


class EducationViewTests(TestCase):
    def setUp(self):
        self.education = Education.objects.create(
            title="S1 Information System",
            institution="University of Indonesia",
            major="Faculty of Computer Science",
            description="GPA = 3.59",
            start_year=2025,
        )

    def test_education_url_is_accessible_and_uses_correct_template(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "education.html")

    def test_education_model_data_appears_in_response(self):
        response = self.client.get(reverse("main:show_education"))

        self.assertContains(response, self.education.title)
        self.assertContains(response, self.education.institution)
        self.assertContains(response, self.education.major)
        self.assertContains(response, "GPA = 3.59")
        self.assertContains(response, "2025")
        self.assertContains(response, "Present")

    def test_empty_education_page_shows_empty_message(self):
        Education.objects.all().delete()

        response = self.client.get(reverse("main:show_education"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No education has been added yet.")

class EducationAuthorizationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.regular = User.objects.create_user(
            username="regular",
            password="TestPassword123!",
        )

        cls.editor = User.objects.create_user(
            username="editor",
            password="TestPassword123!",
        )

        editor_group, _ = Group.objects.get_or_create(name="Editor")
        cls.editor.groups.add(editor_group)

        cls.owner = User.objects.create_superuser(
            username="owner",
            password="TestPassword123!",
        )

        cls.education = Education.objects.create(
            title="S1 Sistem Informasi",
            institution="Universitas Indonesia",
            major="Sistem Informasi",
            description="Belajar pengembangan aplikasi.",
            start_year=2025,
        )

    def setUp(self):
        self.list_url = reverse("main:show_education")
        self.json_url = reverse("main:get_educations_json")
        self.create_url = reverse("main:create_education")

        self.update_url = reverse(
            "main:update_education",
            args=[self.education.pk],
        )

        self.delete_url = reverse(
            "main:delete_education",
            args=[self.education.pk],
        )

        self.star_url = reverse(
            "main:toggle_education_star",
            args=[self.education.pk],
        )

        self.form_data = {
            "title": "S1 Sistem Informasi",
            "institution": "Universitas Indonesia",
            "major": "Sistem Informasi",
            "description": "Deskripsi yang diperbarui.",
            "thumbnail": "",
            "start_year": 2025,
            "end_year": "",
        }

    def test_public_pages_can_be_read_without_login(self):
        for url in [self.list_url, self.json_url]:
            with self.subTest(url=url):
                response = self.client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_visitors_are_redirected_to_login(self):
        # Akses langsung ke URL aksi tetap membutuhkan login.
        for url in [
            self.create_url,
            self.update_url,
            self.delete_url,
            self.star_url,
        ]:
            with self.subTest(url=url):
                response = self.client.post(url, self.form_data)

                self.assertRedirects(
                    response,
                    f"{reverse('main:login')}?next={url}",
                    fetch_redirect_response=False,
                )

    def test_regular_user_cannot_modify_education(self):
        self.client.force_login(self.regular)

        # Form tambah dan update juga tidak boleh dibuka.
        for url in [self.create_url, self.update_url]:
            with self.subTest(method="GET", url=url):
                self.assertEqual(
                    self.client.get(url).status_code,
                    403,
                )

        for url in [
            self.create_url,
            self.update_url,
            self.delete_url,
        ]:
            with self.subTest(method="POST", url=url):
                self.assertEqual(
                    self.client.post(url, self.form_data).status_code,
                    403,
                )

        self.education.refresh_from_db()
        self.assertEqual(
            self.education.description,
            "Belajar pengembangan aplikasi.",
        )
        self.assertEqual(Education.objects.count(), 1)

    def test_editor_can_update_but_cannot_create_or_delete(self):
        self.client.force_login(self.editor)

        self.assertEqual(
            self.client.get(self.update_url).status_code,
            200,
        )

        response = self.client.post(
            self.update_url,
            self.form_data,
        )
        self.assertRedirects(response, self.list_url)

        self.education.refresh_from_db()
        self.assertEqual(
            self.education.description,
            "Deskripsi yang diperbarui.",
        )

        self.assertEqual(
            self.client.get(self.create_url).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(
                self.create_url,
                self.form_data,
            ).status_code,
            403,
        )
        self.assertEqual(
            self.client.post(self.delete_url).status_code,
            403,
        )

        self.assertTrue(
            Education.objects.filter(pk=self.education.pk).exists()
        )
        self.assertEqual(Education.objects.count(), 1)

    def test_owner_can_create_update_and_delete(self):
        self.client.force_login(self.owner)

        response = self.client.post(
            self.create_url,
            self.form_data,
        )
        self.assertRedirects(response, self.list_url)
        self.assertEqual(Education.objects.count(), 2)

        response = self.client.post(
            self.update_url,
            self.form_data,
        )
        self.assertRedirects(response, self.list_url)

        self.education.refresh_from_db()
        self.assertEqual(
            self.education.description,
            "Deskripsi yang diperbarui.",
        )

        response = self.client.post(self.delete_url)
        self.assertRedirects(response, self.list_url)

        self.assertFalse(
            Education.objects.filter(pk=self.education.pk).exists()
        )

    def test_all_logged_in_roles_can_star_and_unstar(self):
        for user in [self.regular, self.editor, self.owner]:
            with self.subTest(user=user.username):
                self.client.force_login(user)

                # Klik pertama memberikan star.
                response = self.client.post(self.star_url)
                self.assertRedirects(response, self.list_url)
                self.assertTrue(
                    self.education.starred_by.filter(
                        pk=user.pk
                    ).exists()
                )
                self.assertEqual(
                    self.education.starred_by.count(),
                    1,
                )

                # Relasi yang sama tidak bisa ditambahkan dua kali.
                self.education.starred_by.add(user)
                self.assertEqual(
                    self.education.starred_by.count(),
                    1,
                )

                # Klik kedua menghapus star.
                response = self.client.post(self.star_url)
                self.assertRedirects(response, self.list_url)
                self.assertEqual(
                    self.education.starred_by.count(),
                    0,
                )

    def test_star_and_delete_reject_get_requests(self):
        self.client.force_login(self.owner)

        for url in [self.star_url, self.delete_url]:
            with self.subTest(url=url):
                self.assertEqual(
                    self.client.get(url).status_code,
                    405,
                )

        # GET tidak boleh mengubah data.
        self.assertEqual(self.education.starred_by.count(), 0)
        self.assertTrue(
            Education.objects.filter(pk=self.education.pk).exists()
        )

    def test_mutations_require_csrf_token(self):
        # Client biasa menonaktifkan pemeriksaan CSRF untuk tes.
        # Client ini secara khusus mengaktifkannya.
        csrf_client = Client(enforce_csrf_checks=True)
        csrf_client.force_login(self.owner)

        for url in [
            self.create_url,
            self.update_url,
            self.delete_url,
            self.star_url,
        ]:
            with self.subTest(url=url):
                response = csrf_client.post(url, self.form_data)
                self.assertEqual(response.status_code, 403)

        self.assertEqual(Education.objects.count(), 1)
        self.assertEqual(self.education.starred_by.count(), 0)

        self.education.refresh_from_db()
        self.assertEqual(
            self.education.description,
            "Belajar pengembangan aplikasi.",
        )

        # Ambil token dari halaman yang memiliki form csrf_token.
        csrf_client.get(self.list_url)
        token = csrf_client.cookies["csrftoken"].value

        response = csrf_client.post(
            self.star_url,
            {"csrfmiddlewaretoken": token},
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            self.education.starred_by.filter(
                pk=self.owner.pk
            ).exists()
        )

    def test_json_excludes_user_information(self):
        self.education.starred_by.add(self.regular)

        response = self.client.get(self.json_url)
        self.assertEqual(response.status_code, 200)

        items = response.json()
        self.assertEqual(len(items), 1)
        self.assertEqual(
            items[0]["pk"],
            str(self.education.pk),
        )

        fields = items[0]["fields"]

        expected_fields = {
            "title",
            "institution",
            "major",
            "description",
            "thumbnail",
            "start_year",
            "end_year",
            "created_at",
            "updated_at",
        }

        self.assertEqual(set(fields), expected_fields)
        self.assertNotIn("starred_by", fields)
        self.assertNotIn("password", fields)
        self.assertNotIn("email", fields)

    def test_json_title_filter_still_works(self):
        response = self.client.get(
            self.json_url,
            {"title": "Sistem Informasi"},
        )
        self.assertEqual(len(response.json()), 1)

        response = self.client.get(
            self.json_url,
            {"title": "Tidak ditemukan"},
        )
        self.assertEqual(response.json(), [])

    def test_action_buttons_follow_user_role(self):
        roles = [
            (None, False, False),
            (self.regular, False, False),
            (self.editor, True, False),
            (self.owner, True, True),
        ]

        for user, can_update, can_create_delete in roles:
            with self.subTest(
                user=user.username if user else "visitor"
            ):
                self.client.logout()

                if user:
                    self.client.force_login(user)

                response = self.client.get(self.list_url)
                self.assertEqual(response.status_code, 200)

                html = response.content.decode()

                self.assertEqual(
                    f'href="{self.create_url}"' in html,
                    can_create_delete,
                )
                self.assertEqual(
                    f'href="{self.update_url}"' in html,
                    can_update,
                )
                self.assertEqual(
                    f'action="{self.delete_url}"' in html,
                    can_create_delete,
                )
# Create your tests here.
