from django.urls import path,include    
from coreapi import views
import coreapi
from .views import HkuMembers,Venues,Visits, VisitedVenuesList, CloseContactsList
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'hku-members',HkuMembers,'hku-member')
router.register(r'venues',Venues,'venue')
router.register(r'visits',Visits,'visit')
urlpatterns = [
    path("",include(router.urls)),
    path('visited-venues', VisitedVenuesList.as_view(), name='visited-venues'),
    path('close-contacts', CloseContactsList.as_view(), name='close-contacts'),

    #path('hku-members2',HkuMembers2.as_view(),name="HkuMembers2")
   
]
