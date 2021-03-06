from celery import shared_task
from django.http import JsonResponse
from .models import Job
import os
import pandas as pd
import numpy as np
import math


@shared_task
def run_diff(metric_id, job_id):
    if metric_id == 'revenue':
        unique_fields = ['date', 'segment_field', 'segment_value_id', 'stat']
    elif metric_id == 'c_revenue':
        unique_fields = ['cohort', 'cohort_id', 'month_nth',
                         'segment_field', 'segment_value_id', 'stat']
    else:
        return JsonResponse({"error_message": "invalid metric_id"})

    base_path = 'diffing/data'
    new_df = pd.read_csv(f'{base_path}/{metric_id}_new.csv')
    old_df = pd.read_csv(f'{base_path}/{metric_id}_old.csv')

    merged_df = pd.merge(new_df, old_df, how='left', left_on=unique_fields,
                         right_on=unique_fields, suffixes=('_new', '_old'))

    def compare_values(df):
        if pd.isna(df['value_new']):
            return 0
        else:
            if pd.isna(df['value_old']):
                return df['value_new']
            else:
                if math.isclose(df['value_new'], df['value_old']):
                    return 0
                else:
                    return df['value_new'] - df['value_old']

    merged_df['value_change'] = merged_df.apply(compare_values, axis=1)

    diff_df = merged_df[merged_df['value_change'] != 0.0]

    file_name = f'{metric_id}_diff_{job_id}.csv'
    dirname = os.path.dirname(__file__)

    diff_df.to_csv(os.path.join(dirname, f'diffed_files/{file_name}'))

    # update job in db
    job = Job.objects.get(pk=int(job_id))
    job.ready = True
    job.file_name = file_name
    job.save()
