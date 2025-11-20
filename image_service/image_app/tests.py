import uuid

from rest_framework import status

from rest_framework.test import APITestCase

from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Image


class ImageAPITestUpload(APITestCase):

    def setUp(self):
        self.image_file = SimpleUploadedFile(
            name='test_image.png',
            content=b'file_content',
            content_type='image/png'
        )
        self.url = 'http://127.0.0.1:8000/api/images/upload_image/'

    def test_upload_image(self):
        response = self.client.post(self.url, {'file': self.image_file}, content_type='image/png')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('status', response.data)

    def test_upload_image_invalid(self):
        response = self.client.post(self.url, {}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('errors', response.data)


class ImageAPITestDelete(APITestCase):
    
    def setUp(self):
        self.image_file = SimpleUploadedFile(
            name='test_image.png',
            content=b'file_content',
            content_type='image/png'
        )
        self.url = 'http://127.0.0.1:8000/api/images/delete_image/'
        self.image = Image.objects.create(file=self.image_file)
    
    def test_delete_image(self):
        response = self.client.delete(f'{self.url}{self.image.id}/')  # Предполагая, что API принимает ID в URL
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_image_not_found(self):
        response = self.client.delete(f'{self.url}9999/') 
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
