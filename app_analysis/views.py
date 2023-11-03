from django.shortcuts import render
from django.conf import settings
import pandas as pd
import os




# Create your views here.
def series(request):
    #views
    path_views = os.path.join(settings.MEDIA_ROOT, 'analysis/data_views.csv')
    views = pd.read_csv(path_views)
    df_views = pd.DataFrame(views)
    df_views_html = df_views.to_html()


    #likes
    path_likes = os.path.join(settings.MEDIA_ROOT, 'analysis/data_likes.csv')
    likes = pd.read_csv(path_likes)
    df_likes = pd.DataFrame(likes)
    df_likes_html = df_likes.to_html()


    return render(request, 'series.html', {
        'df_views_html': df_views_html,
        'df_likes_html':df_likes_html,

    })


def dataframe(request):
    path_data = os.path.join(settings.MEDIA_ROOT, 'analysis/data.csv')
    df_data = pd.read_csv(path_data)
   


    return render(request, 'dataframe.html', {
        
    })