from django.urls import path
from SessionsApp import views

urlpatterns=[
    
    path('metrics/orders', views.SessionApi),
    #path("DataToDB", views.DataToDB)
    
]