from django.apps import AppConfig


class SendemailConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'sendEmail'
    verbose_name = '發電子郵件'


