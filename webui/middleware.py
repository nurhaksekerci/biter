from django.shortcuts import redirect
from django.urls import resolve

class LoginPageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            current_url_name = resolve(request.path_info).url_name
            if current_url_name == 'login':
                return redirect('webui:message_list')
        return self.get_response(request) 