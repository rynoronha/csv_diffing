from django.http import JsonResponse
from diffing.models import Job


def new_job(request, metric_id):
    #TODO: Add your logic here for starting a diffing job
    job = Job.objects.create(metric=metric_id)
    return JsonResponse({"job_id": job.pk, "metric_id": metric_id})


def get_job(request, job_id):
    #TODO: Add your logic here for retrieving a job if is ready
    try:
        job = Job.objects.get(pk=int(job_id))
        return JsonResponse({"job_id": job_id, "metric_id": job.metric})
    except Job.DoesNotExist:
        return JsonResponse({"job_id": None})