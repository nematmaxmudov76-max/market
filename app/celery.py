from celery import Celery
from app.config import settings
from app.utils import send_email


celery = Celery(
    "market_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)


"""
celery orqa fonda uvicorn serverga topshirmasdan 
o'zi emailga message yuborish ishni bajaradi hech kimga halaqit bermasdan
"""


@celery.task(name="send_email_message")
def send_email_message(to_email: str, subject: str, body: str):
    send_email(
        to_email=to_email, subject=subject, body=body
    )  # tartib muhim {to_email, subject, body}
    return True


celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Tashkent",
    enable_utc=True,
)
