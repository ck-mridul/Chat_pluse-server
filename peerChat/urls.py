from django.urls import path 
from . import views 

urlpatterns = [ 

	path('', views.GetAllPeerView.as_view()),
	path('getallmsg/', views.GetAllMessageView.as_view()),
	path('search/', views.SearchView.as_view()),
	path('addfriend/', views.AddFriendView.as_view()),
	path('removefriend/', views.RemoveFriendView.as_view()),
	path('blockcontact/', views.BlockContactView.as_view()),
	path('deletechat/', views.DeleteChatView.as_view()),
 
] 
