from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # This line tells Django: "Go look in core/urls.py for anything starting with api/"
    path('api/', include('core.urls')), 
]