import os

import uuid

import logging

from django.http import FileResponse

from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.views.decorators.cache import cache_page

from rest_framework import viewsets
from rest_framework import status

from rest_framework.decorators import action

from rest_framework.response import Response

from .models import Image
from .forms import ImageUploadForm
from .serializers import ImageSerializer


logger = logging.getLogger(__name__)


# Explicit is better than implicit.
class ImageViewSet(viewsets.ModelViewSet):
    
    serializer_class = ImageSerializer

    queryset = Image.objects.all()

    
    @action(detail=False, methods=['post'])
    def upload_image(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid(): 
           ImageViewSet.save_new_image(form)
           return Response(
               {'status': 'Success!'},
               status=status.HTTP_201_CREATED
           )
        logger.error("Image upload failed with errors: %s", form.errors)
        return Response(
            {'status': 'Failure!'},
            status=status.HTTP_400_bad_request
        )
    
    @action(detail=True, methods=['get'])
    @cache_page(60 * 10)
    def get_image(self, request, pk=None):
        image = get_object_or_404(Image, pk=pk)
        return FileResponse(
            image.file, content_type=(
                'image/%s' % image.file.name.split('.')[-1]
            )
        )
    
    @action(detail=False, methods=['get'])
    @cache_page(60 * 10)
    def all_images(self, request):
        images = Image.objects.all().order_by('-uploaded_at')
        page = self.paginate_queryset(images)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(images, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['delete'])
    def delete_image(self, request, pk=None):
        image = get_object_or_404(Image, pk=pk)
        if os.path.exists(image.file.path):
            os.remove(image.file.path)
            logger.info('Deleted image with pk %s' % pk)
        image.delete()
        return Response(
            {'status': 'Success!'},
            status=status.HTTP_204_NO_CONTENT
        )
    
    @staticmethod
    def save_new_image(form):
        image_file = form.cleaned_data['file']
        image_name = image_file.name
            
        new_file_name = '%s_%s' % (
            uuid.uuid4(), image_name
        )
        image_file.name = new_file_name

        image = form.save(commit=False)
        image.file = image_file
        image.save()
        logger.info("Image uploaded successfully.")


def upload_image_view(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            ImageViewSet.save_new_image(form)
            return redirect('all_images')
    else:
        form = ImageUploadForm()
    return render(
        request, 
        'upload_image.html',
        {'form': form}
    )


def get_image_view(request, pk):
    image = get_object_or_404(Image, pk=pk)
    return FileResponse(
        image.file, content_type=(
            'image/%s' % image.file.name.split('.')[-1]
        )
    )


def all_images_view(request):
    images = Image.objects.all().order_by('-uploaded_at')
    return render(
        request,
        'all_images.html',
        {'images': images}
    )


def delete_image_view(request, pk):
    image = get_object_or_404(Image, pk=pk)
    if request.method == 'POST':
        if os.path.exists(image.file.path):
            os.remove(image.file.path)
        image.delete()
        return redirect('all_images')
    return render(
        request,
        'confirm_delete.html',
        {'image': image}
    )


def home_view(request):
    return render(request, 'home.html')
