from django.contrib import admin
from django.urls import path, include
from .views import login_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', login_view, name='login'),
    

    path('', include('dashboard.urls')),
]