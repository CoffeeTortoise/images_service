from django.urls import path
from django.urls import include

from rest_framework import routers

from . import views


router = routers.SimpleRouter()

router.register(r'images', views.ImageViewSet)

urlpatterns = [
    path(
        'images/', views.upload_image_view, name='upload_image',
    ),
    path(
        'image/<int:pk>/', views.get_image_view, name='get_image'
    ),
    path(
        'image/delete/<int:pk>/', views.delete_image_view, name='delete_image'
    ),
    path(
        'view_images/', views.all_images_view, name='all_images'
    ),
    path(
        '', views.home_view, name='home'
    ),
    path(
        'api/v1/', include(router.urls)
    )
]
