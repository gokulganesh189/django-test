from django.utils.translation import activate

class UserPreferredLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        preferred_language = request.headers.get('Accept-Language', 'en')
        activate(preferred_language)
        request.LANGUAGE_CODE = preferred_language
        return self.get_response(request)
