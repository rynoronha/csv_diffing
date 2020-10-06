<img src="https://app.peelinsights.com/cdn/img/peel_black.svg" width=200>

## Instruction for completing and submitting the challenge:

Thanks for applying to Peel! 
Welcome to our coding challenge for the platform role, this is a space for you to share with us how you work and reason about the problem presented, what things you care about when doing coding work, and how you approach problem solving. As such, through this challenge we are not expecting to check if you know the finest algorithms, have all the right answers to a given situation or if you are the best coder in the world. We believe there are no right or wrong answers, so please make yourself comfortable and focus on what you know best.

Luckily we have done some work before hand of setting up this project with the default Django template, so you can focus on the actual solution.

**Please submit your ideas to us in 1 week (max).** This will give us enough time to review your challenge with the rest of the team before the next interview. During this interview we will take some time to explore together your coding challenge submission, and will ask you any clarifying questions we might have.

Based on previous candidate experiences, we believe **it will take you between 10 and 12 hours to complete the challenge.** 

## Objective

Most times at Peel our platform has to run operations on big datasets that need to be handled fast and optimized to use a minimal memory and CPU footprint, you are tasked to build a task that can do a diff of two given datasets and return the results in an API.


### Datasets

Since Peel supports many different metrics, diffing can change depending on the important keys on each metrics, for the sake of this challenge you will only work with `cohort-revenue` and `revenue`. Another important fact of Peel is that all metrics can be segmented so you need to guarantee the diffing handles correctly values with or without a segment.

For `c-revenue` the unique keys are `cohort`,`cohort_id`,`month_nth`,`[segment_field]`,`[segment_value_id]` and `stat`.
For `revenue` the unique keys are `date`, `[segment_field[`, `[segment_value_id]` and `stat`.

We will make sure to give you CSV datasets for testing for both metrics by email when receiving this challenge. See below for a teaser of how a dataset would look

```
cohort,cohort_id,month_date,month_nth,segment_field,segment_name,segment_value,segment_value_id,stat,value
2015-07-01,15,2015-07-01,,,,,,c-revenue-pc,75.12679951100245
2015-07-01,15,2015-08-01,1,,,,,c-revenue,312241.31
2015-07-01,15,2015-08-01,1,,,,,c-revenue-pc,76.34261858190709
2015-07-01,15,2015-09-01,2,,,,,c-revenue,328424.91
2017-10-01,15,2020-04-01,30,shipping_province,states,Western Australia,Western Australia,c-revenue-pc,136.4535643564356
2017-10-01,15,2020-05-01,31,shipping_province,states,Western Australia,Western Australia,c-revenue,13781.809999999998
2017-10-01,15,2020-05-01,31,shipping_province,states,Western Australia,Western Australia,c-revenue-pc,136.4535643564356
2017-10-01,15,2020-06-01,32,shipping_province,states,Western Australia,Western Australia,c-revenue,13781.809999999998
2017-10-01,15,2020-06-01,32,shipping_province,states,Western Australia,Western Australia,c-revenue-pc,136.4535643564356
2017-10-01,15,2020-07-01,33,shipping_province,states,Western Australia,Western Australia,c-revenue,13781.809999999998
2017-10-01,15,2020-07-01,33,shipping_province,states,Western Australia,Western Australia,c-revenue-pc,136.4535643564356
2017-10-01,15,2020-08-01,34,shipping_province,states,Western Australia,Western Australia,c-revenue,13866.309999999998
2017-10-01,15,2020-08-01,34,shipping_province,states,Western Australia,Western Australia,c-revenue-pc,137.29019801980195
2017-10-01,15,2020-09-01,35,shipping_province,states,Western Australia,Western Australia,c-revenue,13866.309999999998
2017-10-01,15,2020-09-01,35,shipping_province,states,Western Australia,Western Australia,c-revenue-pc,137.29019801980195
```


### Diffing

Given two datasets a new one and an old one, you should return the new datasets that includes only rows that are guarantee to have a different values or new ones. Some values might have very small differences so we recommend using `math.isclose(new_val, old_val):  # Precision of 1e-09`. 

### APIS
`http://localhost:8000/api/diffing/new/<metric_id>`

The API should create a new job/task for running a diff for a given metric, for this challenge is safe to assume you can read the files from disc and the files are mapped for each metric. The only parameter the API reads is the ID of the metric, for example `new/revenue`.

The API should return a job id that can be used to retrieve the diff when is ready.

Response
```
{
  "job_id": 1
}
```

`http://localhost:8000/api/diffing/job/<id>`

For retrieving a CSV download of the final diff we will use this API with the job_id we got previously. In case the job has not finished the API should just return a status code 404 not found. Optionally you can return a status of the job, but you will have to keep tracked of the status while the job is executing.

```
{
  "job_id": 1
  "status": "processing"
}
```

### Async Jobs
We want you to have full flexibility here, at Peel we use `celery` and `rabbitmq` for async jobs, but feel free to use anything you are familiar with to save time, from Python's `multiprocessing` to `concurrent.futures` to `Redis Queue`.


## Technical requirements and Tips
There are a few rules that we would like you to follow during your code challenge:
  - Make sure the diffing is fast without using too much resources, please include in your readme information on how long it takes to diff and approximately how much memory it uses.
  - Feel free to do the diffing manually in pure CSV or with pandas, thou watch out for pandas memory consumption.
  - The Django template comes with a Job model and a sqlite DB, don't waste to much time on DB handling stuff, thou feel free to edit the model as it suits you. 
  - The project uses pipenv for declaring Python dependencies and is set to use Python 3.8 and Django 2.2, you can setup your environment using `pipenv --python 3.8 shell` and then `pipenv install -d`


Your submission should also include a readme file, where you can document your work, describe the features and the architectural decisions that you made. Feel free to share there your thoughts about the challenges that you faced implementing this code. Please include any specific instructions that we might need to test your solution.


## What’s next?
Once you submit your solution, our team will review your code challenge, taking your experience level into account. The sample code provided by you should be in a state considered as a "production" ready - where each requested element is prepared and potentially ready to review with your colleagues.


Good luck!

**“The Challenge” has been created with the sole intention of being used as a guiding document for the current recruitment process. This means we won't be using it (all or parts of it) within our projects.**
