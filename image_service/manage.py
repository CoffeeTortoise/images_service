#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import subprocess

from image_service.settings import DEBUG

IMAGES_DIR = './media/images'


def main():
    fastapi_part = './tesseract_requests.py'
    fastapi_port = 9999
    command = 'fastapi %s %s --port %s' % (
        'dev' if DEBUG else 'run', fastapi_part, fastapi_port
    )
    pc = subprocess.Popen(
        command, shell=True
    )
    if not os.path.exists(IMAGES_DIR):
        os.makedirs(IMAGES_DIR)
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'image_service.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
