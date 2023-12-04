from django.urls import path
from . import views
from django.conf import settings
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    path('register',views.register,name='register'),
    path('login_view',views.login_view,name='login_view'),
    path('logout_view',views.logout_view,name='logout_view'),
    path('verify_ngo',views.verify_ngo,name='verify_ngo'),  
    path('sdg_goal',views.sdg_goal,name='sdg_goal'),  
    path('approve_verification/<int:ngo_id>',views.approve_verification,name='approve_verification'),
    path('reject_verification/<int:ap_id>',views.reject_verification,name='reject_verification'),
    path('project_create',views.project_create,name='project_create'),  
    path('project_apply',views.project_apply,name='project_apply'), 
    path('create_donation',views.create_donation,name='create_donation'),  


    
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)