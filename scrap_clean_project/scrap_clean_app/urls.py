from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from . import views

urlpatterns = [
    path('json_upload/', views.index, name='index'),
    path('view_config/', views.schemename, name='view_schemename'),
    path('config/edit/', views.editconfig, name='editconfig'),
    path('list_config/', views.listconfig, name='listconfig'),
    path('upload/', views.upload, name='upload'),
    
]
urlpatterns += staticfiles_urlpatterns()