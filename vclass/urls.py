from django.contrib import admin
from django.urls import path, include 
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [ 
    path('admin/', admin.site.urls),
    path('api/authentication/', include('authentication.urls')),
    path('api/',include('videoCalling.urls')),
    path('api/chat/',include('chat.urls')),
    path('api/admin/',include('adminside.urls')),
    path('api/payment/',include('payment.urls')),
    path('api/peerchat/',include('peerChat.urls')),
] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()