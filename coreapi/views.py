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

# class HkuMembers2(generics.ListAPIView):
#     queryset = HkuMember.objects.all()
#     serializer_class = HkuMemberSerializer
class HkuMembers(viewsets.ModelViewSet):
    
    queryset = HkuMember.objects.all()
    serializer_class = HkuMemberSerializer
class Venues(viewsets.ModelViewSet):
    
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
class Visits(viewsets.ModelViewSet):
    
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer
