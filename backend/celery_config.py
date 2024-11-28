from celery import Celery

def init_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL'],
        include=['celery_task']
    )
    celery.conf.update(
        broker_transport_options={
            # 'visibility_timeout': 3600,
            'polling_interval': 10.0,
        },
        worker_prefetch_multiplier=1,
        task_acks_late=True
    )

    celery.conf.beat_schedule = {
    'daily-professional-reminders': {
        'task': 'celery_task.send_daily_professional_reminders',
        'schedule': 60 * 60 * 24,
    },
    'monthly-activity-report': {
        'task': 'celery_task.send_monthly_activity_report',
        'schedule':60 * 60 * 24 * 30,
    },
    'check-expired-service-requests': {
        'task': 'celery_task.check_expired_service_requests',
        'schedule': 60 * 60 * 12,
    }
}

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery