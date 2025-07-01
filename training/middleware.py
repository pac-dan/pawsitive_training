class VideoStreamingMiddleware:
    """
    Middleware to add proper headers for video streaming
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Add headers for video files
        if request.path.startswith('/media/training/videos/') and request.path.endswith('.mp4'):
            response['Accept-Ranges'] = 'bytes'
            response['Content-Type'] = 'video/mp4'
            response['Cache-Control'] = 'public, max-age=86400'
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, HEAD, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Range'
        
        return response 