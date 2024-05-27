from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from SessionsApp.models import Sessions
from SessionsApp.serializers import SessionsSerializer
from SessionsApp.DataProcessing import DataToDB
#import psycopg2

# Create your views here.

@csrf_exempt
def SessionApi(request,id=0):
    if request.method=='GET':
        #DataToDB()
        sessions = Sessions.objects.all()
        sessions_serializer=SessionsSerializer(sessions, many=True)
        return JsonResponse(sessions_serializer.data, safe=False)
    elif request.method=='POST':
        #sessions_data=JSONParser().parse(request)
        #sessions_serializer=SessionsSerializer(data=sessions_data)
        #if sessions_serializer.is_valid():
         #sessions_serializer.save()
          #return JsonResponse ("Data added")
        #return JsonResponse("Data not valid", safe=False)
        return JsonResponse('Method not allowed',safe=False)
    elif request.method=='PUT':
        #sessions_data=JSONParser().parse(request)
        #sessions=Sessions.objects.get()
        #sessions_serializer=SessionsSerializer(sessions,data=sessions_data)
        #if sessions_serializer.is_valid():
            #sessions_serializer.save()
            #return JsonResponse("Record updated", safe=False)
        return JsonResponse("Method not allowed",safe=False)
        #return JsonResponse('Method not allowed')
    elif request.method=='DELETE':
        #sessions=Sessions.objects.get()
        #sessions.delete()
        #return JsonResponse('Record deleted', safe=False)
        
        return JsonResponse('Method not allowed',safe=False)
    
DataToDB()