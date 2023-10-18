from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from .models import PostModel
from rest_framework import status
# Create your tests here.
class PostViewSetTests(APITestCase):
    def setUp(self) -> None:
        self.superuser = User.objects.create_superuser(username='adminTest', password='azerty1234', email='adminTest@test.com')
        self.client.force_authenticate(user=self.superuser)
        self.post_data={
            'title':'Test Post Title',
            'body':'Test Post Content',
        }
        self.test_post = PostModel.objects.create(author=self.superuser,**self.post_data)

    def test_list_posts(self):
        response = self.client.get('/posts/')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data), 0)

    def test_create_post_authenticate_user(self):
        response = self.client.post('/posts/', self.post_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(PostModel.objects.count(),2)
        self.assertEquals(PostModel.objects.last().body,'Test Post Content')    

    def test_retreive_post(self):
        response = self.client.get('/posts/{self.test_post.id}')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.assertEquals(response.data['body'], 'Test Post Content')

    def test_partial_update_authenticate_user(self):
        updated_data = {'body':'updated post'}
        response = self.client.patch('/posts/{self.test_post.id}',updated_data, format='json')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        self.test_post.refresh_from_db()
        self.assertEquals(self.test_post.body, 'updated post')

    def test_destroy_post_authenticated_user(self):
        response = self.client.delete('/posts/{self.test_post.id}')
        self.assertEquals(response.status_code, status.HTTP_200_OK)
        with self.assertRaises(PostModel.DoesNotExist):
            PostModel.objects.get(id=self.test_post.id)
    
    def test_destroy_posts_noexistant(self):
        response = self.client.delete('/posts/999')
        self.assertEquals(response.status_code, status.HTTP_404_NOT_FOUND)