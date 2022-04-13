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
def CreateHkuMember(hku_id,name):
    p = HkuMember.objects.create(hku_id=hku_id, name=name)
    
    display=""
    allhkumember = HkuMember.objects.all()
    for hkumember in allhkumember:
        display += str(hkumember)+"<br>"
    return HttpResponse(display)

#not done yet for the following functions
def ViewHkuMember(request):
    display=""
    allhkumember = HkuMember.objects.all()
    for hkumember in allhkumember:
        display += str(hkumember)+"<br>"
    return HttpResponse(display)
def ModifyHkuMember(request):
    display=""
    allhkumember = HkuMember.objects.all()
    for hkumember in allhkumember:
        display += str(hkumember)+"<br>"
    return HttpResponse(display)
def DeleteHkuMember(request):
    display=""
    allhkumember = HkuMember.objects.all()
    for hkumember in allhkumember:
        display += str(hkumember)+"<br>"
    return HttpResponse(display)
