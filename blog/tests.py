from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
from .models import Post
from .forms import PostForm


class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )

    def test_post_creation(self):
        post = Post.objects.create(
            title="Test Title", content="Test Content", author=self.user
        )
        self.assertEqual(post.title, "Test Title")
        self.assertEqual(post.content, "Test Content")
        self.assertEqual(post.author.username, "testuser")
        self.assertIsNotNone(post.created_at)
        self.assertIsNotNone(post.updated_at)

    def test_post_string_representation(self):
        post = Post(title="Sample Title")
        self.assertEqual(str(post), "Sample Title")


class PostFormTest(TestCase):
    def test_valid_form(self):
        data = {"title": "Test Title", "content": "Test Content"}
        form = PostForm(data=data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        data = {"title": "", "content": "Test Content"}
        form = PostForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)


class PostViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.post = Post.objects.create(
            title="Test Post", content="Test Content", author=self.user
        )

    def test_home_view_status_code(self):
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/home.html")

    def test_post_detail_view(self):
        response = self.client.get(
            reverse("post_detail", kwargs={"pk": self.post.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Post")
        self.assertTemplateUsed(response, "blog/post_detail.html")

    def test_post_create_view_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("post_create"))
        self.assertRedirects(
            response, f"{settings.LOGIN_URL}?next={reverse('post_create')}"
        )

    def test_post_create_view_logged_in(self):
        self.client.login(username="testuser", password="testpass")
        response = self.client.get(reverse("post_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "blog/post_form.html")

        # Тестируем создание нового поста
        data = {"title": "New Post", "content": "New Content"}
        response = self.client.post(reverse("post_create"), data)
        self.assertEqual(Post.objects.count(), 2)
        new_post = Post.objects.latest("created_at")
        self.assertEqual(new_post.title, "New Post")
        self.assertEqual(new_post.author.username, "testuser")


class URLsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.post = Post.objects.create(
            title="Test Post", content="Test Content", author=self.user
        )

    def test_home_url_resolves(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_post_detail_url_resolves(self):
        response = self.client.get(f"/post/{self.post.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_invalid_post_detail(self):
        response = self.client.get("/post/999/")
        self.assertEqual(response.status_code, 404)


class TemplateContentTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass"
        )
        self.post = Post.objects.create(
            title="Test Post", content="Test Content", author=self.user
        )

    def test_home_page_displays_posts(self):
        response = self.client.get(reverse("home"))
        self.assertContains(response, "Test Post")
        self.assertContains(response, "Test Content")

    def test_post_detail_page_displays_content(self):
        response = self.client.get(
            reverse("post_detail", kwargs={"pk": self.post.pk})
        )
        self.assertContains(response, "Test Post")
        self.assertContains(response, "Test Content")
