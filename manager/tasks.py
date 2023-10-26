from celery import shared_task


@shared_task
def show_user_fullname(user):
    print(user.full_name)