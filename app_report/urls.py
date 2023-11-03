from django.urls import path
from app_report.views import *


app_name = 'app_report'
urlpatterns = [
    path('report/', report_with_flexmonster, name = 'report_with_flexmonster'),
    path('pivot-data/', pivot_data, name='pivot_data'),
]
