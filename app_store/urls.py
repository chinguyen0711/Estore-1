from django.urls import path
from app_store.views import *


app_name = 'app_store'
urlpatterns = [
    path('', trang_chu, name='trang_chu'),
    path('trang-chu-2/', trang_chu_2, name='trang_chu_2'),
    path('danh-muc/<int:id_subcategory>/', danh_muc, name='danh_muc'),  # danh-muc/0/
    path('san-pham/<int:id_product>/', san_pham, name='san_pham'),      # san-pham/123/
    path('lien-he/', lien_he, name='lien_he'),
    path('rss/', rss, name='rss'),
    path('products-service/', products_service, name='products_service'),
    path('tim-kiem/', tim_kiem, name='tim_kiem'),
]
