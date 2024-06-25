from django.urls import path,re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

app_name = 'evaluations'

urlpatterns = [
    path('', views.evaluation_form, name="evaluation_form"),
    path('result/', views.evaluation_result, name="result"),
    path('export-pdf/', views.ExportPDFView.as_view(), name='export_pdf'),
]

urlpatterns += staticfiles_urlpatterns()