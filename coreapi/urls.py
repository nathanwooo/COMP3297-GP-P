from django.urls import path,include    
from coreapi import views
from .views import HkuMembers,HkuMembers2
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'hku-members',HkuMembers,'hku-member')
urlpatterns = [
    path("",include(router.urls)),
    path('hku-members2',HkuMembers2.as_view(),name="HkuMembers2")
    #path('createhkumember', views.CreateHkuMember),
    
]
