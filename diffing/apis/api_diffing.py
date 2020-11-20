from django.http import JsonResponse
from diffing.models import Job
from diffing.tasks import run_diff
from celery.result import AsyncResult


def new_job(request, metric_id):
    job = Job.objects.create(metric=metric_id)
    result = run_diff.delay(metric_id, job.pk)

    return JsonResponse({"job_id": job.pk, "metric_id": metric_id})


def get_job(request, job_id):
    # TODO: Add your logic here for retrieving a job if is ready
    try:
        job = Job.objects.get(pk=int(job_id))
        if job.ready:
            return JsonResponse({"job_id": job_id, "status": "ready!"})
        else:
            return JsonResponse({"job_id": job_id, "status": "processing"})
    except Job.DoesNotExist:
        return JsonResponse({"job_id": None})
