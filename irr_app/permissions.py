from base_user.utils import UserPosition
from irr_app.models import InspectionReport


def check_user_ir(user, ir):
    return ir in user.mr_irs.all()

"""def engineer_delete_ir(function=None, redirect_field_name=REDIRECT_FIELD_NAME):
    '''
    Decorator for views that checks that the logged in user is a hr user,
    redirects to the log-in page if necessary.
    '''
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.position == UserPosition.Engineer.value and object in u.my_irs.all(),
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator"""
