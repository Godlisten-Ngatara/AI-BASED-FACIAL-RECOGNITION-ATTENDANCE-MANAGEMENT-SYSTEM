from celery import Celery

celery_app = Celery(
    "backend_service",
    broker="redis://172.17.188.100:6379/0",             # Redis as broker
    backend="redis://172.17.188.100:6379/0"             # Optional: store results
)

celery_app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json'], 
    enable_utc=True,
)

celery_app.autodiscover_tasks([
    "backend_service.tasks.cache_attendees"
])
