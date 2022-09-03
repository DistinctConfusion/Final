from django.urls import path

from .views import (
    video_view,
)

app_name = 'video'

urlpatterns = [

    path('<user_id>/call', video_view, name='video_call'),

]