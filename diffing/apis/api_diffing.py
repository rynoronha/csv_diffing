from django.http import JsonResponse, HttpResponse
from diffing.models import Job
from diffing.tasks import run_diff
from celery.result import AsyncResult
import os


def new_job(request, metric_id):
    job = Job.objects.create(metric=metric_id)
    result = run_diff.delay(metric_id, job.pk)

    return JsonResponse({"job_id": job.pk, "metric_id": metric_id})


def get_job(request, job_id):
    try:
        job = Job.objects.get(pk=int(job_id))
        if job.ready:
            dirname = os.path.dirname(__file__)
            file_path = os.path.join(
                dirname, f'../diffed_files/{job.file_name}',)

            with open(file_path, 'r') as f:
                file_data = f.read()

            response = HttpResponse(file_data, content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{job.metric}-diff.csv"'

            return response
        else:
            return JsonResponse({"job_id": job_id, "status": "processing"})
    except Job.DoesNotExist:
        return JsonResponse({"job_id": None})
