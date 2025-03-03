# Setup For Managing Jobs, Tasks or Queues

All Celery related command must be run in the root directory

## Start celery with multiple workers

-Q specifies which queue each worker should consume from. In this command, workers 1 to 3 will consume from the daily_run queue which works with releasing projects everyday and so on while workers 4 and 5 will consume from the mailing_service queue. Worker 6 will listen on the default queue 'celery'

```shell
celery multi start 6 -A jobs -l INFO -Q:1-3 daily_run -Q:4,5 mailing_service -Q:6 celery --pidfile="$HOME/celery/%n.pid" --logfile="$HOME/celery/%n.log"
```

Note that this comand must be run in the root directory.

* [routing](https://docs.celeryq.dev/en/main/getting-started/next-steps.html#routing)
* [starting the worker](https://docs.celeryq.dev/en/main/getting-started/next-steps.html#starting-the-worker)

## Stop Celery

The stop command is asynchronous so it won’t wait for the worker to shutdown. You’ll probably want to use the stopwait command instead, which ensures that all currently executing tasks are completed before exiting:

```shell
celery multi stopwait 5 -A jobs -l INFO --pidfile="$HOME/celery/%n.pid" --logfile="$HOME/celery/%n.log"
```

## Remote Control

You can control and inspect the workers at runtime. For example you can see what tasks the worker is currently working on:

```sh
celery -A jobs inspect active
```

[Read more](https://docs.celeryq.dev/en/main/getting-started/next-steps.html#remote-control)

## Start Celery Beat

Celery beat is the service used for automatically executing tasks with an interval. It is important to perform certain tasks on a daily basis like releasing projects

```sh
celery -A jobs beat --loglevel=INFO
```

Note that this comand must be run in the root directory.
