from django.urls import path
from app_customer.views import *


app_name = 'app_customer'
urlpatterns = [
    path('dang-nhap/', dang_nhap_dang_ky, name='dang_nhap_dang_ky'),
    path('dang-xuat/', dang_xuat, name='dang_xuat'),
    path('thong-tin-cua-toi/', thong_tin_cua_toi, name='thong_tin_cua_toi'),
    path('xuat-bao-cao-don-hang/<int:order_id>/', xuat_bao_cao_don_hang, name='xuat_bao_cao_don_hang'),
]
