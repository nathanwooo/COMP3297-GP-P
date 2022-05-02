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

def get_infectous_hk_time(diagnosis_date):
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
        infectous_date = get_infectous_hk_time(diagnosis_date)

        visits = find_visited_venues(uid, infectous_date, 'venue')
        return visits.values('venue').distinct()


def print_list(qset):
    for r in qset:
        print(r.time)
    print(len(qset))

class InfectousVisit():
    def __init__(self, start, end, venue_code):
        self.start = start
        self.end = end
        self.venue_code = venue_code
    
    def __str__(self):
        return f"visited to {self.venue_code} from {self.start} to {self.end}"

# class VisitRecord():
#     end = None
#     def __init__(self, start, uid):
#         self.start = start
#         self.uid = uid
    
#     def __str__(self):
#         return f"Member {self.uid} Visited to infectous location from {self.start} to {self.end}"

def is_more_than_30_mins(start, end):
    time_range = DateTimeRange(start, end)
    print(time_range)
    return time_range.get_timedelta_second() >= THIRTY_MIN

def get_close_contacts(infectous_visit, uid, close_contacts_uid_set):
    close_contact_visits = Visit.objects.filter(venue = infectous_visit.venue_code).exclude( Q(member=uid) | 
        (Q(Q(event=OUT_EVENT) & Q(time__lte = infectous_visit.start)) | Q(Q(event=IN_EVENT) & Q(time__gte = infectous_visit.end))) ).order_by('time')
    print("Close Contacts")
    print(close_contact_visits)

    start_time_dict = dict()
    # previous_start = infectous_visit.start

    for visit in close_contact_visits:
        # print(start_time_dict)
        member_uid = visit.member
        if visit.event == IN_EVENT:
            # if visit.member not in start_time_dict:
            start_time_dict[member_uid] = visit.time
            # start_time_dict[member_uid] = VisitRecord(visit.time, member_uid)
        elif visit.event == OUT_EVENT:
            if visit.member not in start_time_dict:
                # assume records are valid and no record loss, the in event is before infectous_vist's start time
                if is_more_than_30_mins(infectous_visit.start, visit.time):
                    close_contacts_uid_set.add(visit.member)
            else:
                start_visit_time = start_time_dict[member_uid]
                if is_more_than_30_mins(start_visit_time, visit.time):
                    close_contacts_uid_set.add(visit.member)
                # assume the records are correct
                # del start_time_dict[member_uid]

    # for visit in close_contact_visits:
    #     if visit.event == IN_EVENT:
    #         previous_start = visit.time
    #     elif visit.event == OUT_EVENT:
    #         if is_more_than_30_mins(previous_start, visit.time):
    #             close_contacts_uid_set.add(visit.member)
    print(close_contacts_uid_set)
    return close_contacts_uid_set

IN_EVENT, OUT_EVENT = 'I', 'O'
THIRTY_MIN = 30 * 60
class CloseContactsList(generics.ListAPIView):
    serializer_class = VisitedVenuesSerializer
    queryset = None

    def get_queryset(self):
        parameters = self.request.query_params
        uid = parameters.get('uid')
        diagnosis_date = datetime.strptime(parameters.get('diagnosis-date'), '%Y-%m-%d')  # may need add error handling
        print(diagnosis_date, type(diagnosis_date))
        infectous_date = get_infectous_hk_time(diagnosis_date)

        print(infectous_date)
        visits = find_visited_venues(uid, infectous_date, 'time')
        print_list(visits)
        print("==")
        previous_start = infectous_date
                # previous_start = infectous_date + timedelta(days=1, hours=5)
                # previous_end = None
                # print(previous_start)
                # candidates = visits.exclude(Q(Q(event=OUT_EVENT) & Q(time__lte = previous_start)))
                # print_list(candidates)
                # print(candidates)
        infectous_visit_list = []
        close_contacts_uid_set = set()
        for visit in visits:
            print(visit)
            if visit.event == IN_EVENT:
                previous_start = visit.time
            elif visit.event == OUT_EVENT:
                current_end = visit.time
                if is_more_than_30_mins(previous_start, current_end):
                    infectous_visit = InfectousVisit(previous_start, current_end, visit.venue)
                    get_close_contacts(infectous_visit, uid, close_contacts_uid_set)
                    infectous_visit_list.append(infectous_visit)
                # previous_end = visit.time
            print(visit.time)
        print(infectous_visit_list)
        for infectous_visit in infectous_visit_list:
            print(infectous_visit)
        # return visits
        print(close_contacts_uid_set)
        for member in close_contacts_uid_set:
            print(member.name, member.hku_id)

        return sorted(close_contacts_uid_set, key=lambda x: x.hku_id)

def view_base(request):
    return render(request,'base.html',context=context)
def view_contacts(request):
    return render(request,'contacts.html',context=context)
def view_venues(request):
    return render(request,'venues.html',context=context)



