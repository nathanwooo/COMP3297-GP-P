from django.urls import path
from coreapi import views
urlpatterns = [
    path("hku-members",views.HkuMembers),
    
    path('createhkumember', views.CreateHkuMember),
    
]
