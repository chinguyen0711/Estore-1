from django.urls import path
from app_analysis.views import *


app_name = 'app_analysis'
urlpatterns = [
    path('series/', series, name='series'),
    path('dataframe/', dataframe, name='dataframe'),

]
