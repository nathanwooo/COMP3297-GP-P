from urllib import request
from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from coreapi.models import Venue, HkuMember, Visit
from .serializers import HkuMemberSerializer,VenueSerializer,VisitSerializer, VisitedVenuesSerializer
from rest_framework import generics, viewsets
from datetime import datetime, timedelta, timezone
from pytz import timezone
from datetimerange import DateTimeRange
# Create your views here.
#@api_view(['GET',])
# def HkuMembers(request):
    
#     allhkumember = HkuMember.objects.all()
#     hkumember_serializer = HkuMemberSerializer(allhkumember, many=True)
    
    
#     return Response(hkumember_serializer.data)

# class HkuMembers2(generics.ListAPIView):
#     queryset = HkuMember.objects.all()
#     serializer_class = HkuMemberSerializer
context = {}
class HkuMembers(viewsets.ModelViewSet):
    
    queryset = HkuMember.objects.all()
    serializer_class = HkuMemberSerializer
class Venues(viewsets.ModelViewSet):
    
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
class Visits(viewsets.ModelViewSet):
    
    queryset = Visit.objects.all()
    serializer_class = VisitSerializer

def change2hk_time(diagnosis_date):
    diagnosis_date = diagnosis_date.replace(tzinfo=timezone('Asia/Hong_Kong'))
    # print(timezone('Asia/Hong_Kong'))
    # print(uid)
    print(diagnosis_date, type(diagnosis_date))
    infectous_date = diagnosis_date - timedelta(days=2)
    print(infectous_date, type(infectous_date))
    return infectous_date

def find_visited_venues(uid, infectous_date, order):
    venues = Visit.objects.filter(member=uid, time__gte=infectous_date).order_by(order)
    print(venues)
    return venues

class VisitedVenuesList(generics.ListAPIView):
    serializer_class = VisitedVenuesSerializer
    queryset = None

    def get_queryset(self):
        parameters = self.request.query_params
        uid = parameters.get('uid')
        diagnosis_date = datetime.strptime(parameters.get('diagnosis-date'), '%Y-%m-%d')  # may need add error handling
        print(diagnosis_date, type(diagnosis_date))
        infectous_date = change2hk_time(diagnosis_date)

        visits = find_visited_venues(uid, infectous_date, 'venue')
        return visits.values('venue').distinct()


def print_list(qset):
    for r in qset:
        print(r.time)
    print(len(qset))

class CloseContactsList(generics.ListAPIView):
    serializer_class = VisitedVenuesSerializer
    queryset = None

    def get_queryset(self):
        parameters = self.request.query_params
        uid = parameters.get('uid')
        diagnosis_date = datetime.strptime(parameters.get('diagnosis-date'), '%Y-%m-%d')  # may need add error handling
        print(diagnosis_date, type(diagnosis_date))
        infectous_date = change2hk_time(diagnosis_date)

        print(infectous_date)
        visits = find_visited_venues(uid, infectous_date, 'time')
        print_list(visits)
        in_event, out_event = 'I', 'O'
        print("==")
        previous_start = infectous_date + timedelta(days=1, hours=5)
        previous_end = None
        print(previous_start)
        candidates = visits.exclude(Q(Q(event=out_event) & Q(time__lte = previous_start)))
        print_list(candidates)
        print(candidates)
        # for visit in visits:
        #     print(visit)
        #     if visit.event == in_event:
        #         previous_start = visit.time
        #     elif visit.event == out_event:
        #         previous_end = visit.time
        #     print(visit.time)
        # return visits

def view_base(request):
    return render(request,'base.html',context=context)
def view_contacts(request):
    return render(request,'contacts.html',context=context)
def view_venues(request):
    return render(request,'venues.html',context=context)



