from django.shortcuts import render
from .models import Custom_User,NGOProfile,Verificationrequest,VolunteerApplication,SDG,Donation,Anayltics
from django.contrib.auth import logout
from django.contrib.auth import login,authenticate
from django.http import JsonResponse,HttpResponse
import json

def register(request):
    # if request.method=='GET':
    #     pass
    if request.method=='POST':
        data = json.loads(request.body)
        user_type=data['user_type']
        required_fields=['username','password','email','first_name','last_name']

        for field in required_fields:
            if not data.get(field):
                return JsonResponse({'message':f"Fill the {field}"},status=400)
        if Custom_User.objects.filter(email=data['email']).exists():            
               return JsonResponse({'message': 'A user with this email already exists'}, status=400)
       
        user = Custom_User.objects.create_user(
                username=data['username'],
                email=data['email'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                password=data['password'],
            )

       

        if user_type=='NGO':
            name=data['name']
            mission=data['mission']
           
            NGOProfile.objects.create(
                user=user,
                name=name,
                mission=mission,
            )
            return JsonResponse({'message':'NGO Registered'})
        elif user_type=='volunteer':
           pass
        else:
            return JsonResponse({'message':'Invalid user type'},status=400)
    else:
        return JsonResponse({'message':'wrong method'},status=405)
    
def login_view(request):
       if request.method=='POST': 
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        if not username or not password:
          return JsonResponse({'message':'Fill all the fields'})
        user = authenticate(request, username=username, password=password)
      
        if user is not None:
            if user.is_active:
                login(request, user)
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
       else:
        return JsonResponse({'message': 'Wrong method'}, status=405)

def logout_view(request):
        logout(request)
        return JsonResponse({'message':'user logged out'})     


def        
      
