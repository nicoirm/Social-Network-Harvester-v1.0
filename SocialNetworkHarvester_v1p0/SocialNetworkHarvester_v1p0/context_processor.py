from .settings import DEBUG, DISPLAY_YET_TO_COMES, FACEBOOK_APP_PARAMS, STATICFILES_VERSION

def settings_variables(request):
    print("test")
    return {
        'DEBUG': DEBUG,
        'DISPLAY_YET_TO_COMES': DISPLAY_YET_TO_COMES,
        'STATICFILES_VERSION': STATICFILES_VERSION,
        'FACEBOOK_APP_PARAMS': FACEBOOK_APP_PARAMS,
            }