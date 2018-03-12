from django.views import generic
from django.http import HttpResponse

def not_authorized(request):
    return HttpResponse("No authorized. 403")
