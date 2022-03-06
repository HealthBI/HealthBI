from django.urls import path
from .views import upload_page
from .views import analysis
from .views import index
from .views import upload_csv

urlpatterns = [
    path('', index, name='index'),
    path('upload/', upload_page, name='upload_page'),
    path('', analysis, name='analysis'),
    path('upload/csv/$', upload_csv, name='upload_csv'),

]
