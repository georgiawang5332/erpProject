from django.contrib import admin
from sendEmail.models import SendEmail

# Register your models here.
class SendEmailAdmin(admin.ModelAdmin):
    list_display = ["id", "subject", "message", "from_email", "to_email"]
    list_filter = ['subject']
admin.site.register(SendEmail, SendEmailAdmin)