# CSV Diffing

CSV Diffing is a Python/Django based api that runs diffing jobs in order to compare two large datasets.

## Stack

The api was built with the following stack:

- Python/Django
- SQLlite for the in memory DB
- Pandas for running dataframe diffing analysis and computation
- Celery for performing async diffing jobs
- Heroku-Redis for the async tasks message broker

## Challenges

The main difficult was optimizing speed and memory performance for the diffing jobs. Pandas is a very powerful library for running analyis on large datasets but inevitably will consume relatively large amounts of memory, especially as you increase the amount of data. Ultimately I decided against saving the diffed dataset to the db first to then be converted to a csv file later and instead saved the dataset directly to csv in the file system, and then served that saved file as a response when the job is ready. This could present an issue if we have a large amount of requests, as we would have a large amount of diffed files saved to memory. A possible way to mitigate this is to run regular tasks for deleting old files or to cache the diffed data if it hasn't changed.

## Installation

The project uses pipenv for declaring Python dependencies and is set to use Python 3.8 and Django 2.2.

Set up your virtual environment by running:

```bash
pipenv --python 3.8 shell
```

Install dependencies by running:

```bash
pipenv install -d
```

If you're using pip, you can install dependencies by running:

```bash
pip3 install -r requirements.txt
```

## Starting the Server

From the root of the project, start the Django server by running:

```bash
python manage.py runserver
```

In another terminal, also in the root of the project, start your Celery server by running:

```bash
celery -A platform_challenge worker -l info
```

Now you're good to go!

## API Endpoints

- Starting a new job

```
http://localhost:8000/api/diffing/new/<metric_id>
```

Where `metric_id` is the metric you want to diff. Currently accepting "revenue" or "c_revenue"

Response:

```
{
  "job_id": 1
}
```

- Retrieving an existing job

```
http://localhost:8000/api/diffing/job/<id>
```

Where `id` is the job_id obtained from the new job response.

If the job is still executing, you should see the following response:

```
{
  "job_id": 1
  "status": "processing"
}
```

If the job is ready, you will receive a CSV download of the diffed file.

## Task efficiency

Below are the time and memory usage for each `metric_id` task

- revenue

  - time: approx. 6 seconds
  - RSS memory: 203 MB

- c_revenue
  - time: approx. 30 seconds
  - RSS memory: 706 MB
