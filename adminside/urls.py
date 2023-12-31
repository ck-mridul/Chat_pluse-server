from django.urls import path 
from . import views 

urlpatterns = [ 

	path('listuser/', views.UserListView.as_view()),
	path('blockuser/', views.BlockUserView.as_view()),
 
] 
