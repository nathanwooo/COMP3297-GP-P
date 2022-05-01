from django.urls import path,include    
from coreapi import views
import coreapi
from .views import HkuMembers,Venues,Visits
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'hku-members',HkuMembers,'hku-member')
router.register(r'venues',Venues,'venue')
router.register(r'visits',Visits,'visit')
urlpatterns = [
    path("",include(router.urls)),
    path("view_base",views.view_base),
    path("contacts",views.view_contacts),
    path("venues",views.view_venues),
    #path('hku-members2',HkuMembers2.as_view(),name="HkuMembers2")
   
]
