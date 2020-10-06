from django.urls import path

from .apis import api_diffing

app_name = 'diffing_api'
urlpatterns = [
    path('diffing/new/<metric_id>', api_diffing.new_job, name='new_job'),
    path('diffing/job/<job_id>', api_diffing.get_job, name='get_job'),
]
