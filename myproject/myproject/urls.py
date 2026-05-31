from django.contrib import admin
from django.urls import path
from dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tambah/', views.tambah, name='tambah'),
    path('logout/', views.logout_view, name='logout'),
    path('edit/<int:id>/', views.edit, name='edit'),
    path('hapus/<int:id>/', views.hapus, name='hapus'),
    path('pembayaran/', views.pembayaran, name='pembayaran'),
    path ('mahasiswa/', views.mahasiswa, name='mahasiswa'),
    path('laporan/', views.laporan, name='laporan'),
    path('laporan/<int:id>/', views.detail_laporan, name='detail_laporan'),

    path(
        'mahasiswa/<int:id>/',
        views.detail_mahasiswa,
        name='detail_mahasiswa'
    ),
]