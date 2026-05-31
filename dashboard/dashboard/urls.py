from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tambah/', views.tambah, name='tambah'),
    path('logout/', views.logout, name='logout'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('hapus/<int:id>/', views.hapus, name='hapus'),

    path('pembayaran/', views.pembayaran, name='pembayaran'),
]