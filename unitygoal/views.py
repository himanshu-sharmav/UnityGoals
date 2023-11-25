from django.shortcuts import render
from .models import Custom_User,NGOProfile,Verificationrequest,VolunteerApplication,SDG,Donation,Anayltics
from django.contrib.auth import logout
from django.contrib.auth import login,authenticate
from django.http import JsonResponse,HttpResponse


def register(request):
    

