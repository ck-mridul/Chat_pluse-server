from django.urls import path 
from . import views 
from rest_framework_simplejwt import views as jwt_views 


urlpatterns = [ 
    path('token/', views.UserLoginView.as_view(), name ='token_obtain_pair'), 
	path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name ='token_refresh'), 
	path('register/', views.UserRegisterView.as_view()), 
	path('update/', views.UserProfileUpdateView.as_view()),
	path('adminlogin/', views.AdminLoginView.as_view()),
	
] 
