from django.shortcuts import render
from .models import Custom_User,NGOProfile,Verificationrequest,VolunteerApplication,SDG,Donation,Anayltics,Project
from django.contrib.auth import logout
from django.contrib.auth import login,authenticate
from django.http import JsonResponse,HttpResponse
from django.shortcuts import get_object_or_404

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
            return JsonResponse({'message':'Volunteer Registered'})
            
            
        else:
            return JsonResponse({'message':'Invalid user type'},status=400)
    else:
        return JsonResponse({'message':'wrong method'},status=405)
    
def login_view(request):
       
       if request.method == 'GET':
           user=request.user
        # if user.is_superuser:
           try:
               all_ngos = NGOProfile.objects.all()
               ngos_data = []
               for ngo in all_ngos:
                  if not ngo.is_rejected: 
                   ngo_user = Custom_User.objects.get(pk=ngo.user_id)
                #    verification_request = Verificationrequest.objects.get(ngo_profile=ngo)
                   ngo_data = {
                       "id": ngo_user.id,
                       "username": ngo_user.username,
                       "email": ngo_user.email,
                       "first_name": ngo_user.first_name,
                       "last_name": ngo_user.last_name,
                       "ngo_name": ngo.name,
                       "mission": ngo.mission,
                    #    "verification_document": str(verification_request.document_upload),
                       "verification_status": ngo.verification_status,
                   }
                   ngos_data.append(ngo_data)
               return JsonResponse(ngos_data, safe=False)
           except (NGOProfile.DoesNotExist, Custom_User.DoesNotExist, Verificationrequest.DoesNotExist) as e:
               return JsonResponse({"message": "Error fetching NGO data"}, status=500)
        # else:
        #     return JsonResponse({"message": "Unauthorized"}, status=403)

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
                if user.is_superuser==True:
                    return JsonResponse({'message':'Admin logged in'})

                return JsonResponse({'message':'user logged in'})
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=400)
       else:
        return JsonResponse({'message': 'Wrong method'}, status=405)

def logout_view(request):
        logout(request)
        return JsonResponse({'message':'user logged out'})     



def reject_verification(request, ap_id):
    if request.method == 'POST':
        if not request.user.is_superuser:
            return JsonResponse({'message': 'Unauthorized'}, status=403)

        verification_request = get_object_or_404(Verificationrequest, ngo_profile_id=ap_id, status='Pending')
        ngo_profile = get_object_or_404(NGOProfile, pk=ap_id)

        verification_request.status = 'Rejected'
        verification_request.save()

        ngo_profile.is_rejected = True
        ngo_profile.save()

        return JsonResponse({'message': 'Verification request rejected'}, status=200)
    else:
        return JsonResponse({'message': 'Invalid method'}, status=405)

def  sdg_goal(request):
    
   if request.method=='POST': 
    data=json.loads(request.body)
    name=data['name']
    description=data['description']

    sdgcreate=SDG(
        name=name,
        description=description,
    )       
    sdgcreate.save()
    return JsonResponse({'message':'Goal created'},status=200)
   else:
    return JsonResponse({'message': 'Wrong method'}, status=405) 
      
def project_create(request):
    user = request.user
    if request.method=='GET':
         sdgs = list(SDG.objects.all().values())
         return JsonResponse(sdgs,safe=False)
    if request.method=='POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        status = request.POST.get('status')
        sdgs_input = request.POST.get('sdgs', '') 
        image = request.FILES.get('project_image')
        if not all([title, description, location, status,image]):
            return JsonResponse({'message': 'Please provide all required fields'}, status=400)
        ngo=NGOProfile.objects.filter(user=user).first()
        sdg_ids = [int(sdg_id) for sdg_id in sdgs_input.split(',') if sdg_id.isdigit()]
        new_project=Project.objects.create(
            ngo=ngo,
            title=title,
            description=description,
            location=location,
            status=status,
            image=image
            # sdg=sdg
        )
        # new_project.save()
        sdgs = SDG.objects.filter(id__in=sdg_ids)
        new_project.sdgs.set(sdgs)

        return JsonResponse({'message':'Project created successfully'})
    else:
        return JsonResponse({'message': 'Wrong method'}, status=405) 
    
def project_apply(request):
    user=request.user
    if request.method == 'GET':
        ngo_id = request.GET.get('ngo_id')
        if ngo_id is not None:
            ngo = get_object_or_404(NGOProfile, pk=ngo_id)
            projects = Project.objects.filter(ngo=ngo).values()

        #     project_data = []
        #     for project in projects:
        #         project_info = {
        #     "id": project.id,
        #     "title": project.title,
        #     "description": project.description,
        #     "image": list(project.image),
        #     "location": project.location
        # }
        #         project_data.append(project_info)
            data= list(projects)  
            return JsonResponse(data,safe=False)
    if request.method=='POST':
        data = json.loads(request.body)
        project_id = data['project_id']
        # status = data.get('status') 
        
        project = Project.objects.filter(pk=project_id).first()
        volunteer = Custom_User.objects.filter(pk=user.id).first()

        if not project or not volunteer:
            return JsonResponse({'message': 'Project or volunteer not found'}, status=404)

        
        if VolunteerApplication.objects.filter(volunteer=volunteer, project=project).exists():
            return JsonResponse({'message': 'Volunteer has already applied to this project'}, status=400)

       
        new_application = VolunteerApplication.objects.create(
            volunteer=volunteer,
            project=project,
            # status=s, 
        )

        return JsonResponse({'message': 'Volunteer application submitted successfully'}, status=201)
    else:
        return JsonResponse({'message': 'Wrong method'}, status=405)
    

def verify_ngo(request):
    user = request.user
    if request.method=='GET':
         current_user = request.user
  
         try:
          custom_user = Custom_User.objects.get(pk=current_user.pk)
          ngo_profile = NGOProfile.objects.get(user=current_user)
  
          user_data = {
              "username": custom_user.username,
              "email": custom_user.email,
              "first_name": custom_user.first_name,
              "last_name": custom_user.last_name,
          }
  
          ngo_data = {
              "name": ngo_profile.name,
              "mission": ngo_profile.mission,
              "verification_status":ngo_profile.verification_status
          }
  
          combined_data = {**user_data, **ngo_data}  
  
          return JsonResponse(combined_data)
         except (Custom_User.DoesNotExist, NGOProfile.DoesNotExist):
          return JsonResponse({"message": "User or NGO profile not found"}, status=401)
    if request.method == 'POST':
        # data = json.loads(request.body)
        document_upload = request.FILES.get('document_upload')

        try:
            ngo_profile = user.ngoprofile
        except NGOProfile.DoesNotExist:
            return JsonResponse({'message': 'NGO Profile not found for this user'}, status=404)
        # if not user.is_staff:
        #     return JsonResponse({'message': 'Unauthorized to verify NGOs'}, status=403)

    
        verification_request = Verificationrequest.objects.create(
            ngo_profile=ngo_profile,
            document_upload=document_upload,
            status='Pending',  
        )

        return JsonResponse({'message': 'NGO verification request submitted successfully'}, status=201)
    else:
        return JsonResponse({'message': 'Wrong method'}, status=405)
    



def approve_verification(request,ngo_id):
    user = request.user

    if request.method == 'POST':
        # ngo_id=request.GET.get('ap_id')
        if not user.is_superuser:
            return JsonResponse({'message': 'Unauthorized to approve verifications'}, status=403)

        ngo = get_object_or_404(NGOProfile, pk=ngo_id)

        verification_requests = Verificationrequest.objects.filter(ngo_profile=ngo, status='Pending')

        for verification_request in verification_requests:
            verification_request.status = 'Approved'
            verification_request.save()
        ngo.verification_status=True
        ngo.save()    

        return JsonResponse({'message': f'Verification requests for NGO ID {ngo_id} approved successfully'}, status=200)
    else:
        return JsonResponse({'message': 'Invalid method'}, status=405)



    
