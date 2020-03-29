from django.urls import path
from . import views
urlpatterns = [
        path('',views.index,name='index'),
        path('<int:id>/download/',views.download,name='download'),
        path('post/',views.post,name="post")
]
