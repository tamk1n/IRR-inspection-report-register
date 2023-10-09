from django.contrib.auth.decorators import user_passes_test

REDIRECT_FIELD_NAME = "irr_app:user-login"


def login_required(
    function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='irr_app:user-login'
):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,
        login_url=login_url,
        redirect_field_name=redirect_field_name,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator