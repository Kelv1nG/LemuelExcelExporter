
from django.urls import path
from .views import HomeView, summarize_files

app_name = 'excel_manager'
urlpatterns = [
    path('', HomeView.as_view(), name='excel_input'),
    path('summarize_files', summarize_files, name='summarize_files'),
]
