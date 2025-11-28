import os
import sys

from rest_framework import status

from rest_framework.test import APITestCase
from rest_framework.test import APIClient

from django.core.cache import cache

from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Image


IMAGES_DIR = './media/images'


def create_image_file():
    return SimpleUploadedFile(
        name='some_img.bmp',
        content=b'file_content',
        content_type='image/bmp'
    )


def create_img_if_not_exists():
    if not Image.objects.exists():
        return create_image_file()
    return None


def upload_img_if_not_any():
    img = create_img_if_not_exists()
    if img is not None:
        client = APIClient()
        response = client.post(
            '/api/v1/images/upload_image/', {'name': img.name, 'file': img}, format='multipart'
        )
        if response.status_code != status.HTTP_201_CREATED:
            sys.stderr.write('Unexpected error while creating new image!\n')
            sys.exit(1)
    return img


class ImageAPITestGet(APITestCase):
    
    @classmethod
    def setUpClass(cls):
        cache.clear()
        super().setUpClass()
    
    def setUp(self):
        self.client = APIClient()
        self.url = '/api/v1/images/get_image/?pk=1'
        self.img = upload_img_if_not_any()
    
    def test_get_image(self):
        response = self.client.get(
            self.url
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def tearDown(self):
        if self.img is not None:
            path = os.path.join(IMAGES_DIR, self.img.name)
            if os.path.exists(path):
                os.remove(path)


class ImageAPITestUpload(APITestCase):

    def setUp(self):
        self.image_file = create_image_file()
        self.url = '/api/v1/images/upload_image/'
        self.client = APIClient()

    def test_upload_image_created(self):
        response = self.client.post(
            self.url, {'name': self.image_file.name, 'file': self.image_file}, format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_upload_image_bad_request(self):
        response = self.client.post(
            self.url, {'name': self.image_file.name, }, format='multipart'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def tearDown(self):
        img_path = os.path.join(IMAGES_DIR, self.image_file.name)
        if os.path.exists(img_path):
            os.remove(img_path)
