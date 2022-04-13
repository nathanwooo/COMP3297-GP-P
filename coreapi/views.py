from django.shortcuts import render
from django.http import HttpResponse

from coreapi.models import Venue, HkuMember, Visit
# Create your views here.

def ListHkuMember(request):
    display=""
    allhkumember = HkuMember.objects.all()
    for hkumember in allhkumember:
        display += str(hkumember)+"<br>"
    
    return HttpResponse(display)
def CreateHkuMember(request):
    return HttpResponse("display")
def ViewHkuMember(request):
    return HttpResponse("display")
def ModifyHkuMember(request):
    return HttpResponse("display")
def DeleteHkuMember(request):
    return HttpResponse("display")
