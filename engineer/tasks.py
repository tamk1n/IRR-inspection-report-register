from celery import shared_task

@shared_task
def set_token_inactive(token_id):

    # importing here to prevent circular import error
    from engineer.models import EngineerRegisterationToken

    engineer_register_token = EngineerRegisterationToken.objects.filter(id=token_id).first()
    engineer_register_token.is_expired = True
    print('here')
    engineer_register_token.save()