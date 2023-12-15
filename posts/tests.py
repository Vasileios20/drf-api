from django.contrib.auth.models import User
from .models import Post
from rest_framework import status
from rest_framework.test import APITestCase


class PostListViewTests(APITestCase):
    def setUp(self):
        User.objects.create_user(
            username='testuser', password='testpassword')

    def test_can_list_posts(self):
        testuser = User.objects.get(username='testuser')
        Post.objects.create(owner=testuser, title='test title',)
        response = self.client.get('/posts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)
        # print(len(response.data))

    def test_logged_in_user_can_create_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.post(
            '/posts/', {'title': 'test title'}
        )
        count = Post.objects.count()
        self.assertEqual(count, 1)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # print(response.data)

    def test_logged_out_user_cannot_create_post(self):
        response = self.client.post(
            '/posts/', {'title': 'test title'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PostDetailViewTests(APITestCase):
    def setUp(self):
        testuser = User.objects.create_user(
            username='testuser', password='testpassword')
        testuser1 = User.objects.create_user(
            username='testuser1', password='testpassword')
        Post.objects.create(owner=testuser, title='test title')
        Post.objects.create(owner=testuser1, title='test title 1')

    def test_can_retrieve_post_using_valid_id(self):
        response = self.client.get('/posts/1/')
        self.assertEqual(response.data['title'], 'test title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)

    def test_cannot_retrieve_post_using_invalid_id(self):
        response = self.client.get('/posts/3/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        # print(response.data)

    def test_can_update_post_own_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.put(
            '/posts/1/', {'title': 'updated title'}
        )
        post = Post.objects.filter(id=1).first()
        self.assertEqual(post.title, 'updated title')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # print(response.data)

    def test_user1_cannot_update_post_not_owned(self):
        self.client.login(username='testuser1', password='testpassword')
        response = self.client.put(
            '/posts/1/', {'title': 'updated title'}
        )
        post = Post.objects.filter(id=1).first()
        self.assertEqual(post.title, 'test title')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # print(response.data)

    def test_user1_cannot_update_post(self):
        self.client.login(username='testuser1', password='testpassword')
        response = self.client.put(
            '/posts/1/', {'title': 'updated title'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # print(response.data)

    def test_can_delete_post(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.delete('/posts/1/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # print(response.data)

    def test_logged_out_user_cannot_update_post(self):
        response = self.client.put(
            '/posts/1/', {'title': 'updated title'}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_logged_out_user_cannot_delete_post(self):
        response = self.client.delete('/posts/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user1_cannot_delete_post(self):
        self.client.login(username='testuser1', password='testpassword')
        response = self.client.delete('/posts/1/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # print(response.data)
