import os

DEBUG = True


def main():
    fastapi_part = './image_process.py'
    fastapi_port = 2001
    command = 'fastapi %s %s --port %s' % (
        'dev' if DEBUG else 'run', fastapi_part, fastapi_port
    )
    os.system(command)


if __name__ == '__main__':
    main()
