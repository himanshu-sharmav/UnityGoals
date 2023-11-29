from django.urls import path
from . import views
from django.conf import settings


urlpatterns=[
    path('register',views.register,name='register'),
    path('login_view',views.login_view,name='login_view'),
    path('logout_view',views.logout_view,name='logout_view'),
    path('verify_ngo',views.verify_ngo,name='verify_ngo'),  
    path('sdg_ngo',views.sdg_goal,name='sdg_ngo'),  
    path('approve_verification/<int:ngo_id>',views.approve_verification,name='approve_verification')

]