from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from coreapi.models import Venue, HkuMember, Visit
from .serializers import HkuMemberSerializer,VenueSerializer,VisitSerializer
from rest_framework import generics,viewsets
# Create your views here.
#@api_view(['GET',])
# def HkuMembers(request):
    
#     allhkumember = HkuMember.objects.all()
#     hkumember_serializer = HkuMemberSerializer(allhkumember, many=True)
    
    
#     return Response(hkumember_serializer.data)
# def CreateHkuMember(hku_id,name):
#     p = HkuMember.objects.create(hku_id=hku_id, name=name)
    
#     display=""
#     allhkumember = HkuMember.objects.all()
#     for hkumember in allhkumember:
#         display += str(hkumember)+"<br>"
#     return HttpResponse(display)
class HkuMembers2(generics.ListAPIView):
    queryset = HkuMember.objects.all()
    serializer_class = HkuMemberSerializer
class HkuMembers(viewsets.ModelViewSet):
    queryset = HkuMember.objects.all()
    serializer_class = HkuMemberSerializer
