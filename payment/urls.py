from django.urls import path 
from . import views 

urlpatterns = [ 

	path('', views.PaymentView.as_view()),
	path('success/', views.PaymentSuccessView.as_view()),
 
] 
