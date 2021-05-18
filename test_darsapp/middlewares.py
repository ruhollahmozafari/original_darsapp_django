from datetime import datetime
import jwt
from django.conf import settings
from django.core.exceptions import PermissionDenied
from rest_framework import status
from django.http import JsonResponse
from api.models import User, Role
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

import time

class TimeStampMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith(reverse('api:time')):
            return self.get_response(request)
        if request.path.startswith(reverse('api:manager_report_presence-absence')) or \
            request.path.startswith(reverse('api:manager_report_presence-absence_perclass')) or \
            request.path.startswith(reverse('api:manager_report_score_perclass')):
            return self.get_response(request)
        try: 
            Token = request.headers['Authorization']           
            Token_fields = jwt.decode(Token, None, algorithm='HS512', verify=False)
            if Token_fields['exp'] < datetime.now().timestamp():
                raise ''
            request.user_object = User.objects.get(username=Token_fields['sub'])
            request.user_object.base_roles = [Role.objects.get(id=request.user_object.role).name]
            # settings.SECRET_KEY
        except:
            return JsonResponse({'msg':_("Invalid token.")}, status=status.HTTP_403_FORBIDDEN)
        #some works while request comes
        response = self.get_response(request)
        #some works after response
        return response


class StatsMiddleware(object):
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        start_time = time.time()
        response = self.get_response(request)
        duration = time.time() - start_time
        # Add the header. Or do other things, my use case is to send a monitoring metric
        response["X-Page-Generation-Duration-ms"] = int(duration * 1000)
        return response