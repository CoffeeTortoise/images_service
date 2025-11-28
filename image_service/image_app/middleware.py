import logging


logger = logging.getLogger(__name__)

class RequestLoggingMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_info = {
            'method': request.method,
            'path': request.get_full_path(),
            'headers': dict(request.headers),
            'body': request.body.decode('utf-8', errors='ignore')
        }
        
        logger.info("Request Info: %s" % request_info)

        response = self.get_response(request)

        response_info = {
            'status_code': response.status_code,
            'content_type': response.get('Content-Type'),
        }
        
        logger.info("Response Info: %s" % response_info)

        return response
