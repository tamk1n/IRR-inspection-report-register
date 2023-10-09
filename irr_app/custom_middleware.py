from django.http import HttpResponseNotAllowed
from django.shortcuts import render

class Handle405Middleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)

        if isinstance(response, HttpResponseNotAllowed):
            return render(request, 'irr_app/logout.html', status=405)
        
        return response
