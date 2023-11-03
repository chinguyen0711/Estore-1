from django.urls import path
from app_admin.views import *


app_name = 'app_admin'
urlpatterns = [
    path('dang-ky-2/', dang_ky_2, name = 'dang_ky_2'),
    path('dang-nhap-2/', dang_nhap_2, name = 'dang_nhap_2'),
    path('danh-sach-nguoi-dung/', danh_sach_nguoi_dung, name = 'danh_sach_nguoi_dung'),
    path('dang-xuat-2/', dang_xuat_2, name = 'dang_xuat_2'),
]
