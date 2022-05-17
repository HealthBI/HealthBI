from django.urls import path
from .views import upload_page
from .views import analysis
from .views import index
from .views import upload_csv
from .views import upload_mappings

urlpatterns = [
    path('', index, name='index'),
    path('upload/', upload_page, name='upload_page'),
    path('upload/', upload_page, name='uploadCsvWithMappings'),
    path('analysis/', analysis, name='analysis'),
    path('upload/csv/$', upload_csv, name='upload_csv'),
    path('upload/mappings/$', upload_mappings, name='upload_mappings'),

]
