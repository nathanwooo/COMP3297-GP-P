from django.urls import path
from coreapi import views
urlpatterns = [
    path('listhkumember', views.ListHkuMember),
    path('createhkumember', views.CreateHkuMember),
    path('viewhkumember', views.ViewHkuMember),
    path('modifyhkumember', views.ModifyHkuMember),
    path('deletehkumember', views.DeleteHkuMember),
]
